"""
    @module settings
    Configuration options for changelog generator
"""
from changelog_generator.fetchers import GithubFetcher
from changelog_generator.parsers import (PullIDParser,
                                         MergedBranchParser,
                                         IssueIDParser
                                         )
from changelog_generator.renderers import (BugFixRenderer,
                                           EnhancementRenderer,
                                           FixedIssueRenderer,
                                           MergedPullRenderer
                                           )


## TARGET PROJECT CONFIGURATIONS ##
PROJECT = "balabit/syslog-ng"
CLONE_URL = "git://github.com/balabit/syslog-ng.git"

## FETCHER SETTINGS ##
FETCHER_AUTH_TOKEN = ""
FETCHER_PLUGIN = GithubFetcher

## PARSERS SETTINGS ##
PULL_ID_PARSER = PullIDParser
MERGED_BRANCH_PARSER = MergedBranchParser
ISSUE_ID_PARSER = IssueIDParser

## CHANGELOG CATEGORIES ##
ENHANCEMENT = "Enhancement"
BUGFIX = "BugFix"
FIXED_ISSUE = "Fixed Issue"
MERGED_PULL = "Merged Pull"

## FETCHER ISSUE LABELS ##
BUG_LABEL = "bug"
ENHANCEMENT_LABEL = "enhancement"

## CHANGELOG RENDERING SETTINGS ##
BUGFIX_SECTION_HEADER = "Bug Fixes"
ENHANCEMENT_SECTION_HEADER = "Enhancements"
FIXED_ISSUE_SECTION_HEADER = "Fixed Issues"
MERGED_PULL_SECTION_HEADER = "Merged Pull Requests"
BUGFIX_ENTRY_RENDERER = BugFixRenderer
ENHANCEMENT_ENTRY_RENDERER = EnhancementRenderer
FIXED_ISSUE_ENTRY_RENDERER = FixedIssueRenderer
MERGED_PULL_ENTRY_RENDERER  = MergedPullRenderer
