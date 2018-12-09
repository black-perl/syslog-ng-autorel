package gitminer

import (
	"fmt"
	"regexp"
	"testing"

	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/goroutinepool"
)

func TestRegexMatching(t *testing.T) {
	str := "Merg 123 e pull request #2401 from 123 #2344 Kokan/binary-hexoctal "
	re := regexp.MustCompile("#([0-9]+)")
	k := re.FindString(str)
	fmt.Println(k)
}

func TestGetMergeRequest(t *testing.T) {
	pool := goroutinepool.NewGoRoutinePool(2, 10, 1)
	gm, err := GetMiner("../../../temp/syslog-ng", "balabit", "syslog-ng", "<token>", "./temp", pool)
	if err != nil {
		panic(err)
	}
	firstCommit := "7be16513a3722488f5e3224a39f7076e6167f72b"
	lastCommit := "82a7a012353143314d8482b7f249e56367a4da59"

	// find commits
	commits, err := gm.getMergeCommits(firstCommit, lastCommit)
	if err != nil {
		panic(err)
	}
	//fmt.Println(commits)

	// parse commits for merge request ids
	mergeReqsIDs, err := gm.getParsedMergeRequestIDs(commits)
	fmt.Println(mergeReqsIDs)

	// fetch the merge requests
	mergeRequests, err := gm.getMergeRequests(mergeReqsIDs)
	panic(err)
	fmt.Println(len(mergeRequests))
}
