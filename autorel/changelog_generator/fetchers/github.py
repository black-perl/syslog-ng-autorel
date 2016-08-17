"""
    @module github
    @class GithubFetcher
    - To support GitLab and other platforms, similar helper
      classes should be crafted
"""
import functools
import logging
import sys
from github import Github
from changelog_generator.structures import (PullRequest,
                                            Issue,
                                            Contributor,
                                            Commit
                                            )
from changelog_generator.main import Fetcher


class GithubFetcher(Fetcher):
    """
        Helper class to fetch Pull Requests,Issues etc.
        information from Github
    """
    def __init__(self, auth_token, project):
        super(GithubFetcher, self).__init__("Github Fetcher",
                                            "Provides methods for fetching pull requests,\
                                             issues, commits etc. from Github"
                                            )
        self._cli = Github(auth_token)
        self._repo_obj = self._cli.get_repo(project)
        # Configure logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        channel = logging.StreamHandler(sys.stdout)
        channel.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        channel.setFormatter(formatter)
        self._logger.addHandler(channel)

    @functools.lru_cache(maxsize=None)
    def get_pull(self, pull_id):
        """
            Get details of a pull request.
            Should return a PullRequest instance
        """
        self._logger.debug("Fetching pull request : #{0}".format(pull_id))
        pull_id = int(pull_id)
        pull_req_obj = self._repo_obj.get_pull(pull_id)
        body = pull_req_obj.body
        url = pull_req_obj.html_url
        title = pull_req_obj.title
        contributor_name = pull_req_obj.user.name or pull_req_obj.user.login
        contributor_email = pull_req_obj.user.email
        contributor_url = pull_req_obj.user.html_url
        contributor = Contributor(contributor_name,
                                  contributor_email,
                                  contributor_url
                                  )
        return PullRequest(title,
                           body,
                           contributor,
                           url
                           )

    @functools.lru_cache(maxsize=None)
    def get_issue(self, issue_id, pull_id=None, commit=None):
        """
            Get details of an issue
            -  An issue can be associated with an optional
               pull request
            -  A commit object carrying contributor infromation
        """
        self._logger.debug("Fetching issue : #{0}".format(issue_id))
        issue_id = int(issue_id)
        linked_pull_obj = None
        if pull_id:
            pull_id = int(pull_id)
            linked_pull_obj = self.get_pull(pull_id)
        issue_obj = self._repo_obj.get_issue(issue_id)
        body = issue_obj.body
        url = issue_obj.html_url
        title = issue_obj.title
        issue_opener = Contributor(issue_obj.user.name or issue_obj.user.login,
                                   issue_obj.user.email,
                                   issue_obj.user.html_url)
        labels_list = issue_obj.labels
        labels = []
        for label_obj in labels_list:
            labels.append(label_obj.name)
        if linked_pull_obj:
            issue_closer = linked_pull_obj.contributor
        elif commit:
            issue_closer = Contributor(commit.author.name,
                                       commit.author.email,
                                       None
                                       )
        issue_contributors = []
        issue_contributors.append(issue_opener)
        issue_contributors.append(issue_closer)
        return Issue(title,
                     body,
                     labels,
                     url,
                     issue_contributors
                     )

    @functools.lru_cache(maxsize=None)
    def get_commit_list(self, pull_id):
        """
            Get linked commits to a pull request
        """
        self._logger.debug("Fetching pull commits : #{0}".format(pull_id))
        pull_id = int(pull_id)
        pull_obj = self._repo_obj.get_pull(pull_id)
        paginated_commit_list = pull_obj.get_commits()
        commit_list = []
        for commit_obj in paginated_commit_list:
            commit_message = commit_obj.commit.message
            commit_sha = commit_obj.commit.sha
            c = Commit(commit_sha,
                       commit_message
                       )
            commit_list.append(c)
        return commit_list
