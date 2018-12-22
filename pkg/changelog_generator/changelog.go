package changelog_generator

type ChangelogSectionType int32

const (
	TextSectionType         ChangelogSectionType = 0
	MergeRequestSectionType ChangelogSectionType = 1
)
