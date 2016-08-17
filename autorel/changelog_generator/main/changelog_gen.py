"""
    @module chnagelog_gen
    @class ChnagelogGenerator
"""
import pygit2
import logging
import sys
from changelog_generator.settings import (ENHANCEMENT,
                                          BUGFIX,
                                          FIXED_ISSUE,
                                          MERGED_PULL,
                                          BUG_LABEL,
                                          ENHANCEMENT_LABEL
                                          )
from changelog_generator.structures import (PullRequest,
                                            Issue,
                                            Contributor
                                            )
from .helpers import ChangelogEntry
from .changelog_renderer import ChangelogRenderer


class ChangelogGenerator(object):
    """
        The Changelog Generator class
    """
    categories = (
        BUGFIX,
        ENHANCEMENT,
        FIXED_ISSUE,
        MERGED_PULL
    )
    __parser = None
    __fetcher = None

    @classmethod
    def configure(cls, parser, fetcher):
        cls.__parser = parser
        cls.__fetcher = fetcher

    def __init__(self, repo_path, last_tagged_commit):
        self._repo = pygit2.Repository(repo_path)
        self._last_tagged_commit = last_tagged_commit
        self._entries = {} # Generated ChangelogEntry objects
        for entry in self.categories:
            self._entries[entry] = []
        self._commits = []
        self._commit_map = {} # Traversal record keeping of commits
        self._issues_map = {} # Traversal record keeping of issues
        # Configure logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        channel = logging.StreamHandler(sys.stdout)
        channel.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        channel.setFormatter(formatter)
        self._logger.addHandler(channel)

    def _mark_commit_node(self, commit):
        """
            Mark a commit node visited
        """
        self._commit_map[commit.hex] = True

    def _mark_issue_node(self, issue_id):
        """
            Mark a issue node visited
        """
        self._issues_map[issue_id] = True

    def _get_commit_node_status(self, commit):
        """
            Check if a commit node is visited or not
        """
        return self._commit_map[commit.hex]

    def _get_issue_node_status(self, issue_id):
        """
            Check if a issue node is visited or not
        """
        if issue_id not in self._issues_map.keys():
            return False
        return self._issues_map[issue_id]

    def _generate_commit_map(self):
        """
            Collect all commits from the last tag point
            and initialise the structures
        """
        for commit in self._repo.walk(self._repo.head.target,pygit2.GIT_SORT_TOPOLOGICAL):
            if commit.hex == self._last_tagged_commit:
                break
            else:
                self._commits.append(commit)
                self._commit_map[commit.hex] = False

    def _add_changelog_entry(self, entry_obj):
        """
            Add an entry to the changelog
        """
        if isinstance(entry_obj,PullRequest):
            category = MERGED_PULL
            changelog_entry = ChangelogEntry(category,
                                             entry_obj.contributor,
                                             entry_obj.url,
                                             entry_obj.title
                                             )
        elif isinstance(entry_obj,Issue):
            if BUG_LABEL in entry_obj.labels:
                category = BUGFIX
            elif ENHANCEMENT_LABEL in entry_obj.labels:
                category = ENHANCEMENT
            else:
                category = FIXED_ISSUE
            changelog_entry = ChangelogEntry(category,
                                             entry_obj.contributors,
                                             entry_obj.url,
                                             entry_obj.title
                                             )
        elif isinstance(entry_obj,ChangelogEntry):
            changelog_entry = entry_obj
            category = entry_obj.category

        self._entries[category].append(changelog_entry)

    def _parse_commits_for_merge_nodes(self):
        """
            Parse the merge commit messages for the pull request identifiers
            or the branch names
        """
        merge_commits = []
        self._pull_ids = []

        for commit in self._commits:
            # Normal merge commit nodes
            if len(commit.parents) >= 2:
                merge_commits.append(commit)
            # Squashed commit nodes
            elif commit.author.name != commit.committer.name:
                merge_commits.append(commit)

        for commit in merge_commits:
            # Case 1 : It is a local checkout
            # Case 2 : It is a pull request merge
            merged_branch = self.__parser.parse_merged_branch(commit.message)
            pull_request_id = self.__parser.parse_pull_id(commit.message)
            if merged_branch:
                # Create changelog entry for the merged branch
                contributor = Contributor(commit.author.name,
                                          commit.author.email,
                                          None
                                          )
                changelog_entry = ChangelogEntry(MERGED_PULL,
                                                 contributor,
                                                 None,
                                                 "{0} : {1}".format(merged_branch,
                                                                    commit.message.split('\n')[0])
                                                 )
                self._add_changelog_entry(changelog_entry)
            elif pull_request_id:
                self._pull_ids.append(pull_request_id)
            else:
                # these are commits corresponding to a merge
                pass

    def _parse_commits_for_issue_nodes(self):
        """
            Parses the commits messages for the issue ids
        """
        issue_commit_list = []
        for commit in self._commits:
            if not self._get_commit_node_status(commit):
                issue_ids = self.__parser.parse_issue_id(commit.message)
                if issue_ids:
                    for issue_id in issue_ids:
                        issue_commit_list.append(tuple((
                                                    commit,
                                                    issue_id
                                                )))
                self._mark_commit_node(commit)
        # Create changelog entries for all the independent issues
        for element in issue_commit_list:
            issue_id = element[1]
            commit = element[0]
            if not self._get_issue_node_status(issue_id):
                issue_obj = self.__fetcher.get_issue(issue_id,
                                                     commit=commit
                                                     )
                self._add_changelog_entry(issue_obj)

    def _extract_linked_issues(self):
        """
            Extract issues linked to pull requests
        """
        issue_pull_list = []
        for pull_id in self._pull_ids:
            pull_obj = self.__fetcher.get_pull(pull_id)
            issue_ids = self.__parser.parse_issue_id(pull_obj.body)
            if issue_ids:
                for issue_id in issue_ids:
                    issue_pull_list.append(tuple((
                                            pull_id,
                                            issue_id
                                          )))
            else:
                self._add_changelog_entry(pull_obj)

        # Create changelog entries for all the issues liked with pull requests
        for pull_id,issue_id in issue_pull_list:
            self._mark_issue_node(issue_id)
            issue_obj = self.__fetcher.get_issue(issue_id,
                                                 pull_id=pull_id
                                                 )
            self._add_changelog_entry(issue_obj)

    def generate(self):
        """
            Generate the changelog according to last provided tag
        """
        self._logger.info("Generating commit map.")
        self._generate_commit_map()
        self._logger.info("Parsing commits for merge nodes.")
        self._parse_commits_for_merge_nodes()
        self._logger.info("Extracting linked issues.")
        self._extract_linked_issues()
        self._logger.info("Parsing commits for issue nodes.")
        self._parse_commits_for_issue_nodes()


    def render(self, file_path=None):
        """
            Render the changelog in markdown format
        """
        self._logger.info("Converting chnagelog to markdown format.")
        renderer = ChangelogRenderer(self._entries)
        return renderer.render(file_path)


if __name__ == "__main__":
    generator = ChangelogGenerator()
    generator.generate()
    generator.render()
