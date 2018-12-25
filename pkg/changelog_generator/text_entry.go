package changelog_generator

import (
	"encoding/json"

	"github.com/satori/go.uuid"
)

type TextEntry struct {
	ID      uuid.UUID
	Content string
}

func NewTextEntry(content string) TextEntry {
	return TextEntry{
		ID:      uuid.NewV4(),
		Content: content,
	}
}

func (textEntry TextEntry) ToString() string {
	resp, _ := json.Marshal(textEntry)
	return string(resp)
}
