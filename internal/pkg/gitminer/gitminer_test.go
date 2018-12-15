package gitminer

import (
	"fmt"
	"testing"

	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/goroutinepool"
)

func TestGetMergeRequest(t *testing.T) {
	pool := goroutinepool.NewGoRoutinePool(2, 10, 1)
	//Using "../../../" still not nice, `git rev-parse --show-toplevel` could tell the current repository root path
	//The changelog generator could use the current git repository, as it should work with any other.
	//Like releasing a first version of this tool should be made with this tool
	gm, err := GetMiner("../../../", "darxtrix", "syslog-ng-autorel", "<token>", "./temp", pool)
	if err != nil {
		panic(err)
	}
	firstCommit := "7ee5deaf1fa8b5ffaba8c3bdc4496f0c3dd558ec"
	lastCommit := "b97accac4b4849fd7c82a9aef0da0ca4171c8eb4"

	mergeRequests, err := gm.GetMergeRequests(firstCommit, lastCommit)
	fmt.Println(len(mergeRequests))
	if err != nil {
		panic(err)
	}
}
