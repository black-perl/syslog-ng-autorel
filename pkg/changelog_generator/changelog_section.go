package changelog_generator

import (
	"encoding/json"

	"github.com/satori/go.uuid"
)

type ChangelogSection struct {
	ID               uuid.UUID
	Description      string
	changelogEntries map[uuid.UUID]interface{}
}

func newChangelogSection(sectionDesc string) ChangelogSection {
	return ChangelogSection{
		ID:               uuid.NewV4(),
		Description:      sectionDesc,
		changelogEntries: make(map[uuid.UUID]interface{}),
	}
}

func (changelogSec ChangelogSection) addEntry(entryId uuid.UUID, entry interface{}) interface{} {
	changelogSec.changelogEntries[entryId] = entry
	return entry
}

func (changelogSec ChangelogSection) getEntry(entryID string) (interface{}, bool) {
	entryUUID, _ := uuid.FromString(entryID)
	val, isFound := changelogSec.changelogEntries[entryUUID]
	return val, isFound
}

func (changelogSec ChangelogSection) removeEntry(entryId string) {
	entryUUID, _ := uuid.FromString(entryId)
	delete(changelogSec.changelogEntries, entryUUID)
}

func (changelogSec ChangelogSection) ToString() string {
	resp, _ := json.Marshal(changelogSec)
	return string(resp)
}
