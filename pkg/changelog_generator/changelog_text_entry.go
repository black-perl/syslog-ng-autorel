package changelog_generator

import (
	"encoding/json"

	"github.com/satori/go.uuid"
)

type ChangelogTextEntry struct {
	ID      uuid.UUID
	content string
}

func newChangelogTextEntry(content string) ChangelogTextEntry {
	return ChangelogTextEntry{
		ID:      uuid.NewV4(),
		content: content,
	}
}

func (cte ChangelogTextEntry) ToString() string {
	resp, _ := json.Marshal(cte)
	return string(resp)
}
