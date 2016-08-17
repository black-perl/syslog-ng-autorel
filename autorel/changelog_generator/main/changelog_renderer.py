"""
    @module chnagelog_renderer
    @class ChangelogRenderer
    - Controls rendering of changelog to markdown
"""
import tempfile
import os
from changelog_generator.settings import (BUGFIX_SECTION_HEADER,
                                          ENHANCEMENT_SECTION_HEADER,
                                          FIXED_ISSUE_SECTION_HEADER,
                                          MERGED_PULL_SECTION_HEADER,
                                          BUGFIX_ENTRY_RENDERER,
                                          ENHANCEMENT_ENTRY_RENDERER,
                                          FIXED_ISSUE_ENTRY_RENDERER,
                                          MERGED_PULL_ENTRY_RENDERER
                                          )
from changelog_generator.settings import (BUGFIX,
                                          ENHANCEMENT,
                                          FIXED_ISSUE,
                                          MERGED_PULL
                                          )


class ChangelogRenderer(object):
    """
        Entry point for all renderers
    """
    def __init__(self, entries):
        self._renderers = {
            BUGFIX : BUGFIX_ENTRY_RENDERER,
            ENHANCEMENT : ENHANCEMENT_ENTRY_RENDERER,
            FIXED_ISSUE : FIXED_ISSUE_ENTRY_RENDERER,
            MERGED_PULL : MERGED_PULL_ENTRY_RENDERER
        }
        self._section_headers = {
            BUGFIX : BUGFIX_SECTION_HEADER,
            ENHANCEMENT : ENHANCEMENT_SECTION_HEADER,
            FIXED_ISSUE : FIXED_ISSUE_SECTION_HEADER,
            MERGED_PULL : MERGED_PULL_SECTION_HEADER
        }
        self._categories = [
            BUGFIX,
            ENHANCEMENT,
            FIXED_ISSUE,
            MERGED_PULL
        ]
        self._entries = entries

    def render(self, file_path):
        """
            Writes the markdown changelog to a file
        """
        if not file_path:
            file_path = os.path.join(tempfile.mkdtemp(),
                                     "changelog.md"
                                     )
        f = open(file_path,'w')
        for category in self._categories:
          if len(self._entries[category]) != 0:
            print(self._section_headers[category], file=f)
            print("=============================", file=f)
            for entry in self._entries[category]:
                renderer = self._renderers[category]
                rendered_value = renderer(entry).render()
                print("{0} {1}".format("*",rendered_value),
                      file=f
                      )
            print("\n", file=f)
        f.close()
        return file_path
