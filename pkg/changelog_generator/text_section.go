package changelog_generator

import (
	"encoding/json"

	"github.com/satori/go.uuid"
)

type TextSection struct {
	ID             uuid.UUID
	Type           ChangelogSectionType
	changelogEntry TextEntry
	Name           string
}

func NewTextSection(sectionName string) TextSection {
	return TextSection{
		ID:   uuid.NewV4(),
		Type: TextSectionType,
		Name: sectionName,
	}
}

func (textSec TextSection) AddOrReplaceContent(content string) {
	if (textSec.changelogEntry != TextEntry{}) {
		textSec.changelogEntry.setContent(content)
	} else {
		textSec.changelogEntry = NewTextEntry(content)
	}
}

func (textSec TextSection) GetContent() string {
	var entry TextEntry
	entry = textSec.changelogEntry
	return entry.getContent()
}

func (textSec TextSection) ToString() string {
	resp, _ := json.Marshal(textSec)
	return string(resp)
}
