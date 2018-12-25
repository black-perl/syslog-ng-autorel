package changelog_generator

type MergeRequestSection struct {
	ChangelogSection
}

func NewMergeRequestSection(sectionDesc string) MergeRequestSection {
	return MergeRequestSection{
		ChangelogSection: newChangelogSection(sectionDesc),
	}
}

func (mergeReqSec MergeRequestSection) AddEntry(entry MergeRequestEntry) MergeRequestEntry {
	addedEntry := mergeReqSec.addEntry(entry.ID, entry)
	return addedEntry.(MergeRequestEntry)
}

func (mergeReqSec MergeRequestSection) GetEntry(entryID string) (MergeRequestEntry, bool) {
	entry, found := mergeReqSec.getEntry(entryID)
	if found {
		return entry.(MergeRequestEntry), found
	}
	return entry.(MergeRequestEntry), found
}

func (mergeReqSec MergeRequestSection) RemoveEntry(entryId string) {
	mergeReqSec.removeEntry(entryId)
}
