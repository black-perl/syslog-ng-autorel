"""
    @module id_parsers
    @classes PullIDParser, MergedBranchParser, IssueIDParser
    Implement any parsers here
"""
import re
from changelog_generator.main import TokenParser


class PullIDParser(TokenParser):
    """
        Parses pull request id from commit message
        => msg : Merge pull request #1234 from username/branch
        => pull_id : 1234
    """
    def __init__(self, commit_msg):
        super(PullIDParser, self).__init__("pull_id",
                                           "Parses pull request id from commit message"
                                           )
        self._set_input(commit_msg)

    def parse(self):
        regexp = r"merge\s+pull\s+request\s+#(\d+)"
        self._result = re.findall(regexp,
                                  self._input,
                                  re.IGNORECASE
                                  )


class MergedBranchParser(TokenParser):
    """
        Parses branch name from commit message
        => msg : Merge from user/master
        => branch_name : user/master
    """
    def __init__(self, commit_msg):
        super(MergedBranchParser, self).__init__("merged_branch",
                                                 "Parses pull request id from commit message"
                                                 )
        self._set_input(commit_msg)

    def parse(self):
        regexp = r"merge\s+branch\s+(\S+)"
        self._result = re.findall(regexp,
                                  self._input,
                                  re.IGNORECASE
                                  )


class IssueIDParser(TokenParser):
    """
        Parses the issue id from commit message or
        pull request body
        => msg : Fixes #1234
        => issue_id : 1234
    """
    def __init__(self, msg):
        super(IssueIDParser, self).__init__("issue_id",
                                            "Parses issue ids from commit message or\
                                            pull request body"
                                            )
        self._set_input(msg)

    def parse(self):
        regexp = r"fixe?s?\s+#(\d+)"
        self._result = re.findall(regexp,
                                  self._input,
                                  re.IGNORECASE)
