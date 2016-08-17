"""
    @module helpers
    @class ChangelogEntry
"""


class ChangelogEntry(object):
    """
        Defines a changelog entry
    """
    def __init__(self, category, contributors, url, text):
        self._category = category
        if type(contributors) == list:
            self._contributors = contributors
        else:
            self._contributors = []
            self._contributors.append(contributors)
        self._url = url
        self._text = text

    @property
    def url(self):
        return self._url

    @property
    def text(self):
        return self._text

    @property
    def contributors(self):
        return self._contributors

    @property
    def category(self):
        return self._category
