"""
    @module entry_renderer
    @class EntryRenderer
    - Base class for all entry renderers
"""


class EntryRenderer(object):
    """
        The class controls the rendering of a ChangelogEntry instance.
        All changelog entry renderers must subclass this.
    """
    def __init__(self, entry_obj):
        self._entry = entry_obj
        self._name = "EntryRenderer"
        self._description = "Class for rendering ChangelogEntry instances"
        self._value = None

    def _set_value(self):
        raise NotImplementedError("Entry rendering logic not implemented")

    def render(self):
        self._set_value()
        return self._value

    def entry_instance(self):
        return self._entry

    def __str__(self):
        return "{0} : {1}".format(self._name,
                                  self._description
                                  )
