from changelog_generator.main import RepositoryParser
from changelog_generator.main import ChangelogGenerator
from changelog_generator.settings import (FETCHER_PLUGIN,
                                          PULL_ID_PARSER,
                                          MERGED_BRANCH_PARSER,
                                          ISSUE_ID_PARSER,
                                          FETCHER_AUTH_TOKEN,
                                          PROJECT
                                          )


RepositoryParser.set_pull_id_parser(PULL_ID_PARSER)
RepositoryParser.set_merged_branch_parser(MERGED_BRANCH_PARSER)
RepositoryParser.set_issue_id_parser(ISSUE_ID_PARSER)

parser = RepositoryParser()
fetcher = FETCHER_PLUGIN(FETCHER_AUTH_TOKEN, PROJECT)
ChangelogGenerator.configure(parser,
                             fetcher
                             )
