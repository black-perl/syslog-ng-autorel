"""
    @module chnagelog_structures
    @classes Contributor, PullRequest, Issue, Commit
    - Changelog generator accepts values as instances
      of the following classes and all Fetcher instances
      should return instances of these classes only
"""


class Contributor(object):
    """
        Defines a contributor
    """

    def __init__(self, name, email, url):
        self._name = name
        self._email = email
        self._url = url

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def url(self):
        return self._url


class PullRequest(object):
    """
        Defines a PullRequest
    """

    def __init__(self, title, body, contributor, url):
        self._title = title
        self._body = body
        self._contributor = contributor
        self._url = url

    @property
    def title(self):
        return self._title

    @property
    def body(self):
        return self._body

    @property
    def contributor(self):
        return self._contributor

    @property
    def url(self):
        return self._url


class Issue(object):
    """
        Defines an Issue
    """

    def __init__(self, title, body, labels,
            url, contributors=None):
        self._title = title
        self._body = body
        self._labels = labels
        self._url = url
        if type(contributors) == list:
            self._contributors = contributors
        else:
            self._contributors = []
            self._contributors.append(contributors)


    @property
    def title(self):
        return self._title

    @property
    def body(self):
        return self._body

    @property
    def url(self):
        return self._url

    @property
    def labels(self):
        return self._labels

    @property
    def contributors(self):
        '''
            Issue contributors
        '''
        return self._contributors


class Commit(object):
    """
        Defines a commit
    """

    def __init__(self, sha, message):
        self._sha = sha
        self._message = message

    @property
    def hex(self):
        return self._sha

    @property
    def message(self):
        return self._message
