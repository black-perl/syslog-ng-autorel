"""
    @module bugfix_renderer
    @class BugfixRenderer
"""
from changelog_generator.main import EntryRenderer


class BugFixRenderer(EntryRenderer):
    """
        The class controls the rendering of a bugfix entry
        in the changelog
    """
    def __init__(self, entry_obj):
        super(BugFixRenderer, self).__init__(entry_obj)
        self._name = "BugfixRenderer"
        self._description = "Class for rendering bug fix information in changelog"

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
