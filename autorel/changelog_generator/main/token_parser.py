"""
    @module token_parser
    @class TokenParser
"""


class TokenParser(object):
    """
        Parses tokens from the text input
    """
    def __init__(self, type_, description):
        self._type = type_
        self._description = description
        self._result = None

    def _set_input(self, text):
        self._input = text

    def _parser(self):
        raise NotImplementedError("No parsers implemented in TokenParser")

    def _parse(self):
        self._result = self._parser(self._input)

    @property
    def result(self):
        return self._result

    def __str__(self):
        return "Parser type<{0}> : {1}".format(self._type,
                                               self._description)
