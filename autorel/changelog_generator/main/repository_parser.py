"""
    @module repository_parser
    @class RepositoryParser
    - All child parsers must register here
"""


class RepositoryParser(object):
    """
        Entry point for child parsers
    """
    __pull_id_parser = None
    __merged_branch_parser = None
    __issue_id_parser = None

    @classmethod
    def set_pull_id_parser(cls, parser):
        cls.__pull_id_parser = parser

    @classmethod
    def set_merged_branch_parser(cls, parser):
        cls.__merged_branch_parser = parser

    @classmethod
    def set_issue_id_parser(cls, parser):
        cls.__issue_id_parser = parser

    def parse_pull_id(self, input_text):
        parser_obj = self.__pull_id_parser(input_text)
        parser_obj.parse()
        result = parser_obj.result
        if len(result) > 1:
            raise Exception('Repository Parser: Invalid input_text')
        elif result:
            return result[0]


    def parse_merged_branch(self, input_text):
        parser_obj = self.__merged_branch_parser(input_text)
        parser_obj.parse()
        result = parser_obj.result
        if len(result) > 1:
            raise Exception('Repository Parser: Invalid input_text')
        elif result:
            return result[0]

    def parse_issue_id(self, input_text):
        parser_obj = self.__issue_id_parser(input_text)
        parser_obj.parse()
        # Multiple issues can be fixed at a time
        return parser_obj.result
