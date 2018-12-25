package changelog_generator

type TextSection struct {
	ChangelogSection
}

func NewTextSection(sectionDesc string) TextSection {
	return TextSection{
		ChangelogSection: newChangelogSection(sectionDesc),
	}
}

func (textSec TextSection) AddEntry(entry TextEntry) TextEntry {
	addedEntry := textSec.addEntry(entry.ID, entry)
	return addedEntry.(TextEntry)
}

func (textSec TextSection) GetEntry(entryID string) (TextEntry, bool) {
	entry, found := textSec.getEntry(entryID)
	if found {
		return entry.(TextEntry), found
	}
	return entry.(TextEntry), found
}

func (textSec TextSection) RemoveEntry(entryId string) {
	textSec.removeEntry(entryId)
}
