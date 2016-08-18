import tempfile
import os
from autorel import settings as global_settings


PROJECT = global_settings.PROJECT

PACKAGE = "syslog-ng"

DEBIAN_CHANGELOG = '''
{PACKAGE_NAME} ({PACKAGE_VERSION}) {RELEASE_TAG}; urgency=low

  * New upstream version.

 -- BalaBit Development Team <devel@balabit.hu>  {CURRDATE}

Local variables:
mode: debian-changelog
End:
'''

GITHUB_AUTH_TOKEN = global_settings.GITHUB_AUTH_TOKEN
                       
TZ_OFFSET = "+05:30"

PROJECT_CLONE_URL = "https://github.com/black-perl/syslog-ng.git"

PROJECT_CLONE_PATH = os.path.join(tempfile.mkdtemp(),
								  PACKAGE
								  )

COMMITTER_NAME = "Ankush Sharma"

COMMITTER_EMAIL = "ankprashar@gmail.com"

VERSION_FILE = "VERSION"

SOURCE_TARBALL_DOCKERFILE = "/home/ank/test/syslog-ng-autorel/autorel/dockerfiles/source-tarball-build"

DEBIAN_SOURCE_DOCKERFILE =  "/home/ank/test/syslog-ng-autorel/autorel/dockerfiles/debian-source-build"

PULL_REQUEST_TITLE = "New Release"

PULL_REQUEST_BODY = "Autorel released syslog-ng"

DEBIAN_CHANGELOG_FILE = "debian/changelog"

SOURCE_MOUNT_DIRECTORY = "/home"
