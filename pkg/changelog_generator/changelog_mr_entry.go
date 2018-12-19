package changelog_generator

import (
	"encoding/json"

	"github.com/darxtrix/syslog-ng-autorel/internal/pkg/gitservercli"
	"github.com/satori/go.uuid"
)

type ChangelogMREntry struct {
	ID uuid.UUID
	gitservercli.MergeRequest
}

func newChangelogMREntry(content string, mergeRequest gitservercli.MergeRequest) ChangelogMREntry {
	return ChangelogMREntry{uuid.NewV4(), mergeRequest}
}

func (cme ChangelogMREntry) ToString() string {
	resp, _ := json.Marshal(cme)
	return string(resp)
}
