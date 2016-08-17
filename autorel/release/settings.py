import tempfile
import os


PROJECT = "black-perl/syslog-ng"

PACKAGE = "syslog-ng"

DEBIAN_CHANGELOG = '''
{PACKAGE_NAME} {PACKAGE_VERSION} {RELEASE_TAG}; urgency=low

  * New upstream version.

 -- BalaBit Development Team <devel@balabit.hu>  {CURRDATE}

Local variables:
mode: debian-changelog
End:
'''

OBS_USER = ""

OBS_PASS = ""

OSC_CONFIG_FILE = "obs_config"

OBS_PROJECT = "home:laszlo_budai:syslog-ng-gsoc-autorel"

OBS_PACKAGE = "syslog-ng-autorel"

GITHUB_AUTH_TOKEN = ""
                       
TZ_OFFSET = "+05:30"

PROJECT_CLONE_URL = "https://github.com/black-perl/syslog-ng.git"

PROJECT_CLONE_PATH = tempfile.mkdtemp()

COMMITTER_NAME = "Ankush Sharma"

COMMITTER_EMAIL = "ankprashar@gmail.com"

VERSION_FILE = "VERSION"

SOURCE_TARBALL_DOCKERFILE = os.path.abspath("../dockerfiles/source-tarball-build")

DEBIAN_SOURCE_DOCKERFILE = os.path.abspath("../dockerfiles/debian-source-build") 

PULL_REQUEST_TITLE = "New Release"

PULL_REQUEST_BODY = "Autorel released syslog-ng"

DEBIAN_CHANGELOG_FILE = "debian/changelog.in"

SOURCE_MOUNT_DIRECTORY = "/home"
