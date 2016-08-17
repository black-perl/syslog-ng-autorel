"""
    @module fixed_issue_renderer
    @class FixedIssueRenderer
"""
from changelog_generator.main import EntryRenderer


class FixedIssueRenderer(EntryRenderer):
    """
        The class controls the rendering of a fixed issue
        entry in the changelog
    """
    def __init__(self, entry_obj):
        super(FixedIssueRenderer, self).__init__(entry_obj)
        self._name = "FixedIssueRenderer"
        self._description = "Class for rendering fixed issues information in changelog"

    def _set_value(self):
        self._template = "{entry_info} {contributor_info}"
        entry_info = "{0}  [Link]({1})".format(self._entry.text,
                                         self._entry.url
                                         )
        contributor_info = ""
        for contributor in self._entry.contributors:
            contributor_name = contributor.name
            contributor_address = contributor.url or contributor.email
            contributor_info += " [{0}]({1}) ".format(contributor_name,
                                                     contributor_address
                                                     )
        self._value = self._template.format(entry_info = entry_info,
                                            contributor_info = contributor_info
                                            )
