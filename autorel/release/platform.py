"""
    @module platform
    @class GithubPlatform
    - Abstracts out the platform dependence of the release cycle
    - All platfroms such as Github, Gitlab etc. comply with the API
"""
import datetime
from github import (Github,
                    InputGitTreeElement,
                    InputGitAuthor
                    )
from .settings import (GITHUB_AUTH_TOKEN,
                       TZ_OFFSET
                       )


class GithubPlatform(object):
    """
        Exposes higher level platform API
    """
    def __init__(self, project):
        self._project = project
        self._client = Github(GITHUB_AUTH_TOKEN)
        self._repo = self._client.get_repo(self._project)

    @property
    def _contributor(self):
        date = datetime.datetime.now().isoformat()
        date += TZ_OFFSET
        return InputGitAuthor(name=self._contributor_name,
                              email=self._contributor_email,
                              date=date
                              )

    def set_committer(self, name, email):
        """
            Set a git committer/author info
        """
        self._contributor_name = name
        self._contributor_email = email

    def get_tagged_commit(self, tag):
        """
            Get the SHA value of the commit tagged with tag
        """
        repo = self._client.get_repo('balabit/syslog-ng') ##hardcoded
        if not tag.startswith("tags/"):
            tag = "tags/" + tag
        ref_object = repo.get_git_ref(tag)
        tag_sha = ref_object.object.sha
        tag_object = repo.get_git_tag(tag_sha)
        linked_commit_sha = tag_object.object.sha
        return linked_commit_sha

    def get_current_release(self):
        """
            Get the latest release tag
        """
        repo = self._client.get_repo('balabit/syslog-ng') ##hardcoded
        releases = []
        for release in repo.get_releases():
            releases.append(release)
        current_release = releases[0]
        return current_release.tag_name

    def create_new_branch(self, orig_branch, new_branch):
        """
            Creates a new branch from the orig_branch
        """
        if not orig_branch.startswith("heads/"):
            orig_branch = "heads/" + orig_branch
        if not new_branch.startswith("refs/heads/"):
            new_branch = "refs/heads/" + new_branch
        # Get the SHA value of the latest commit on the orig_branch
        orig_branch_ref = self._repo.get_git_ref(orig_branch)
        latest_commit_sha = orig_branch_ref.object.sha
        self._repo.create_git_ref(ref=new_branch,
                                  sha=latest_commit_sha
                                  )

    def create_commit(self, orig_branch, file_path, commit_message, file_name):
        """
            Creates a commit to the orig_branch by adding a file given by file_path
            and using a provided commit_message
        """
        ## find the latest commit SHA on the orig_branch
        if not orig_branch.startswith("heads/"):
            orig_branch = "heads/" + orig_branch
        orig_branch_ref = self._repo.get_git_ref(orig_branch)
        latest_commit_sha = orig_branch_ref.object.sha
        ## find the base tree to be written out
        latest_commit = self._repo.get_commit(latest_commit_sha)
        base_tree = latest_commit.commit.tree
        ## create a new tree
        with open(file_path,'r') as f:
            file_contents = f.read()
        # specifications required to create a new tree
        new_tree_specs = InputGitTreeElement(path=file_name,
                                             mode="100644",
                                             type="blob",
                                             content=file_contents
                                             )
        new_tree = self._repo.create_git_tree(base_tree=base_tree,
                                              tree=[new_tree_specs]
                                              )
        ## create a new commit on the new_tree
        parent_commits = [latest_commit.commit]
        created_commit = self._repo.create_git_commit(message=commit_message,
                                                      tree=new_tree,
                                                      parents=parent_commits,
                                                      author=self._contributor,
                                                      committer=self._contributor
                                                      )
        ## update the orig_branch to reference created_commit
        orig_branch_ref.edit(sha=created_commit.sha)
        return created_commit.sha

    def create_pull_request(self, title, body, branch_a, branch_b):
        """
            Sends a pull request from branch_a to branch_b
        """
        self._repo.create_pull(title=title,
                               body=body,
                               head=branch_a,
                               base=branch_b
                               )

    def create_annoted_tag(self, tag_name, message, ref_sha, ref_type):
        """
            Creates an annoted tag
        """
        # create a tag object
        tag = self._repo.create_git_tag(tag=tag_name,
                                        message=message,
                                        object=ref_sha,
                                        type=ref_type,
                                        tagger=self._contributor
                                        )
        # Register the tag object
        tag_ref = "refs/tags/{0}".format(tag_name)
        self._repo.create_git_ref(ref=tag_ref,
                                  sha=tag.sha
                                  )

    def create_release(self, tag, name, message, draft=True, prerelease=False):
        """
            Creates a release draft
        """
        self._repo.create_git_release(tag=tag,
                                      name=name,
                                      message=message,
                                      draft=draft,
                                      prerelease=prerelease
                                      )
