"""
    @module fetchers
    @class Fetcher
    - Base class for all Fetchers
"""

class Fetcher(object):
    """
        The class provides methods for fetching changelog structures
        such as pull requests, issues etc. from the repository
        All subclasses must provide the implementation of the fetcher functions
    """
    def __init__(self, name, description):
        self._name = name
        self._description = description

    def get_pull(self):
        raise NotImplementedError("Pull request fetcher function not implemented")

    def get_issue(self):
        raise NotImplementedError("Issue fetcher function not implemented")

    def get_commit_list(self):
        raise NotImplementedError("Commit list fetcher function not implemented")

    def __str__(self):
        return "{0} : {1}".format(self._name,self._description)

