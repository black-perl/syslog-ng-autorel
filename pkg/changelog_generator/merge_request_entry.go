package changelog_generator

import (
	"encoding/json"

	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/gitservercli"
	"github.com/satori/go.uuid"
)

type MergeRequestEntry struct {
	ID uuid.UUID
	gitservercli.MergeRequest
}

func newMergeRequestEntry(content string, mergeRequest gitservercli.MergeRequest) MergeRequestEntry {
	return MergeRequestEntry{uuid.NewV4(), mergeRequest}
}

func (mergeReqEntry MergeRequestEntry) ToString() string {
	resp, _ := json.Marshal(mergeReqEntry)
	return string(resp)
}
