package gitminer

import (
	"context"
	"fmt"
	"os"
	"sync"

	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/cache"
	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/gitservercli"
	"github.com/pkg/errors"
	"gopkg.in/libgit2/git2go.v27"
)

type gitServerClient interface {
	GetMergeRequest(context.Context, string, string, int) (gitservercli.MergeRequest, error)
}

type gitObjectsCache interface {
	Put(string, interface{})
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
}

var gitMinerInstance *GitMiner
var once sync.Once

func GetMiner(repositoryPath string, gitServerAPIAccessToken string, gitObjectsCacheFilePath string) (*GitMiner, error) {
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
		}
	})
	return gitMinerInstance, errorInInstantiation
}

func (gm *GitMiner) GetMergeRequests(firstCommit string, lastCommit string) ([]*git.Commit, error) {
	repo, err := git.InitRepository(gm.repositoryPath, false)
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
	var mergeCommits []*git.Commit
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
			mergeCommits = append(mergeCommits, commit)
		}
	}
	if revWalkErr != nil {
		return nil, errors.Wrap(revWalkErr, fmt.Sprintf("Error during history traversal of the repository"))
	}
	return mergeCommits, nil
}
