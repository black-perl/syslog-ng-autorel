package gitminer

import (
	"fmt"
	"testing"
)

func TestGetMergeRequest(t *testing.T) {
	//Using "../../../" still not nice, `git rev-parse --show-toplevel` could tell the current repository root path
	//The changelog generator could use the current git repository, as it should work with any other.
	//Like releasing a first version of this tool should be made with this tool
	gm, err := GetMiner("../../../temp/syslog-ng", "balabit", "syslog-ng", "<access-token-here>", "./temp")
	if err != nil {
		panic(err)
	}
	firstCommit := "7be16513a3722488f5e3224a39f7076e6167f72b"
	lastCommit := "82a7a012353143314d8482b7f249e56367a4da59"

	mergeRequests, err := gm.GetMergeRequests(firstCommit, lastCommit)
	fmt.Println(len(mergeRequests))
	if err != nil {
		panic(err)
	}
}
