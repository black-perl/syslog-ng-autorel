package changelog_generator

import (
	"encoding/json"

	"github.com/satori/go.uuid"
)

type MergeRequestSection struct {
	ID               uuid.UUID
	Type             ChangelogSectionType
	changelogEntries map[uuid.UUID]MergeRequestEntry
	Name             string
}

func NewMergeRequestSection(sectionName string) MergeRequestSection {
	return MergeRequestSection{
		ID:               uuid.NewV4(),
		Type:             MergeRequestSectionType,
		changelogEntries: make(map[uuid.UUID]MergeRequestEntry),
		Name:             sectionName,
	}
}

func (mergeReqSec MergeRequestSection) AddEntry(entry MergeRequestEntry) MergeRequestEntry {
	mergeReqSec.changelogEntries[entry.ID] = entry
	return entry
}

func (mergeReqSec MergeRequestSection) GetEntry(entryID string) (MergeRequestEntry, bool) {
	var entry MergeRequestEntry
	entryUUID, _ := uuid.FromString(entryID)
	val, isFound := mergeReqSec.changelogEntries[entryUUID]
	if isFound {
		entry = val
	}
	return entry, isFound
}

func (mergeReqSec MergeRequestSection) RemoveEntry(entryId string) {
	entryUUID, _ := uuid.FromString(entryId)
	delete(mergeReqSec.changelogEntries, entryUUID)
}

func (mergeReqSec MergeRequestSection) ToString() string {
	resp, _ := json.Marshal(mergeReqSec)
	return string(resp)
}
