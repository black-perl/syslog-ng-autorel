package gitminer

import (
	"context"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/cache"
	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/gitservercli"
	"github.com/pkg/errors"
	"gopkg.in/libgit2/git2go.v27"
)

type gitServerClient interface {
	GetMergeRequest(context.Context, string, string, int) (gitservercli.MergeRequest, error)
}

type gitObjectsCache interface {
	Set(string, interface{})
	Get(string) (interface{}, bool)
	Delete(string)
	Flush()
	Persist() error
	RegisterCachableType(interface{})
}

type GitMiner struct {
	repositoryPath     string
	gsc                gitServerClient
	goc                gitObjectsCache
	cachedObjectsTypes []interface{}
	repositoryUser     string
	repositoryName     string
}

var gitMinerInstance *GitMiner
var once sync.Once

func (gm *GitMiner) getMergeCommits(firstCommit string, lastCommit string) ([]git.Commit, error) {
	repo, err := git.OpenRepository(gm.repositoryPath)
	if err != nil {
		return nil, errors.Wrap(err, fmt.Sprintf("Error in intiliazing git repository"))
	}
	revWalkPtr, err := repo.Walk()
	if err != nil {
		return nil, errors.Wrap(err, fmt.Sprintf("Error in intiliazing git reverse walk pointer"))
	}
	revWalkPtr.Sorting(git.SortTopological | git.SortTime)
	err = revWalkPtr.PushHead()
	if err != nil {
		return nil, errors.Wrap(err, fmt.Sprintf("Error in determing HEAD of the repository %s", gm.repositoryPath))
	}
	startingCommitObject, err := git.NewOid(lastCommit)
	if err != nil {
		return nil, errors.Wrap(err, fmt.Sprintf("Invalid last commit %s supplied", lastCommit))
	}
	// configure reverse walk to start from last commit
	revWalkPtr.Push(startingCommitObject)
	nextOId := new(git.Oid)
	var revWalkErr error
	var mergeCommits []git.Commit
	for {
		revWalkErr = revWalkPtr.Next(nextOId)
		if revWalkErr != nil {
			break
		}
		if nextOId.String() == firstCommit { // stop traversal
			break
		}
		commit, revWalkErr := repo.LookupCommit(nextOId)
		if revWalkErr != nil {
			break
		} else if commit.ParentCount() == 2 { // merge commit
			mergeCommits = append(mergeCommits, *commit)
		}
	}
	if revWalkErr != nil {
		return nil, errors.Wrap(revWalkErr, fmt.Sprintf("Error during history traversal of the repository"))
	}
	return mergeCommits, nil
}

func (gm *GitMiner) getParsedMergeRequestIDs(commits []git.Commit) ([]int, error) {
	var match string
	var mergeRequestIDs []int
	re, _ := regexp.Compile("#([0-9]+)")
	for _, commit := range commits {
		match = re.FindString(commit.Message())
		if len(match) < 0 {
			return mergeRequestIDs, errors.New(fmt.Sprintf("Not able to parse merge request id from the commit message %s", commit.Message()))
		}
		// remove the # character from the start
		mergeRequestID := strings.Trim(match, "#")
		mergeRequestIDInt, err := strconv.Atoi(mergeRequestID)
		if err != nil {
			return mergeRequestIDs, errors.Wrap(err, fmt.Sprintf("Not able to integer value from merge request id %s", mergeRequestID))
		}
		mergeRequestIDs = append(mergeRequestIDs, mergeRequestIDInt)
	}
	return mergeRequestIDs, nil
}

func (gm *GitMiner) getMergeRequests(mergeRequestsIDs []int) ([]gitservercli.MergeRequest, error) {
	var mergeRequests []gitservercli.MergeRequest
	ctx := context.Background()
	mergeRequestsChan := make(chan gitservercli.MergeRequest, len(mergeRequestsIDs))
	mergeRequestIDsChan := make(chan int, len(mergeRequestsIDs))
	quit := make(chan int, 1)
	err := make(chan error, 1)
	// schedule goroutines in the pool
	for i := 0; i < len(mergeRequestsIDs); i++ {
		go func() {
			select {
			case <-quit:
				return
			case mergeRequestID := <-mergeRequestIDsChan:
				cacheKey := fmt.Sprintf("%s_%s_%d", gm.repositoryUser, gm.repositoryName, mergeRequestID)
				cachedMergeRequest, isFound := gm.goc.Get(cacheKey)
				if isFound {
					mergeRequestsChan <- cachedMergeRequest.(gitservercli.MergeRequest)
				} else {
					mergeRequest, err1 := gm.gsc.GetMergeRequest(ctx, gm.repositoryUser, gm.repositoryName, mergeRequestID)
					if err1 != nil {
						err <- err1
					} else {
						gm.goc.Set(cacheKey, mergeRequest)
						mergeRequestsChan <- mergeRequest
					}
				}
				return
			}
		}()
	}
	for i := 0; i < len(mergeRequestsIDs); i++ {
		mergeRequestIDsChan <- mergeRequestsIDs[i]
	}
	for {
		select {
		case err2 := <-err: // prevent the pending goroutines from running in case of err
			close(quit)
			return mergeRequests, err2
		case mergeRequest := <-mergeRequestsChan:
			mergeRequests = append(mergeRequests, mergeRequest)
			if len(mergeRequests) == len(mergeRequestsIDs) { // all goroutines ran successfully
				return mergeRequests, nil
			}
		case <-time.After(10 * time.Second):
			return mergeRequests, errors.New("Error timeout while getting data")
		}
	}
}

func GetMiner(repositoryPath string, repositoryUser string, repositoryName string, gitServerAPIAccessToken string, gitObjectsCacheFilePath string) (*GitMiner, error) {
	var errorInInstantiation error
	once.Do(func() {
		cachedObjectsTypes := []interface{}{}
		cachedObjectsTypes = append(cachedObjectsTypes, gitservercli.MergeRequest{})
		// instantiate cache for storing the fechted objects
		goc, err := cache.NewCache(gitObjectsCacheFilePath, cachedObjectsTypes)
		if err != nil {
			errorInInstantiation = err
		}
		// instantiate the gitServerCli to access the git server api
		gsc := gitservercli.NewGitServerClient(gitServerAPIAccessToken)
		// check if the supplied repository path is valid or not
		if _, err := os.Stat(repositoryPath); err != nil {
			errorInInstantiation = errors.Wrap(err, fmt.Sprintf("Reposiory path validation failed"))
		}
		gitMinerInstance = &GitMiner{
			repositoryPath:     repositoryPath,
			gsc:                gsc,
			goc:                goc,
			cachedObjectsTypes: cachedObjectsTypes,
			repositoryUser:     repositoryUser,
			repositoryName:     repositoryName,
		}
	})
	return gitMinerInstance, errorInInstantiation
}

func (gm *GitMiner) GetMergeRequests(firstCommit string, lastCommit string) ([]gitservercli.MergeRequest, error) {
	var mergeRequests []gitservercli.MergeRequest
	mergeCommits, err := gm.getMergeCommits(firstCommit, lastCommit)
	if err != nil {
		return mergeRequests, err
	}
	mergeRequestIDs, err := gm.getParsedMergeRequestIDs(mergeCommits)
	if err != nil {
		return mergeRequests, err
	}
	mergeRequests, err = gm.getMergeRequests(mergeRequestIDs)
	if err != nil {
		return mergeRequests, err
	}
	err = gm.goc.Persist() // persist cache
	if err != nil {
		return mergeRequests, err
	}
	return mergeRequests, nil
}
