package changelog_generator

import (
	"encoding/json"

	"github.com/satori/go.uuid"
)

type TextEntry struct {
	ID      uuid.UUID
	content string
}

func NewTextEntry(content string) TextEntry {
	return TextEntry{
		ID:      uuid.NewV4(),
		content: content,
	}
}

func (textEntry TextEntry) getContent() string {
	return textEntry.content
}

func (textEntry TextEntry) setContent(content string) string {
	textEntry.content = content
}

func (textEntry TextEntry) ToString() string {
	resp, _ := json.Marshal(textEntry)
	return string(resp)
}
