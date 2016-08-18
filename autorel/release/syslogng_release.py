"""
    @module : syslogng_release
    @class : SyslogNgRelease
    - SyslogNgRelease class governs the release process
      of syslog-ng
"""
import pygit2
import os
import datetime
import shutil
import tempfile
import logging
import sys
from autorel.changelog_generator import ChangelogGenerator
from autorel.utils import Docker
from autorel.build_helpers import (get_debian_source_building_commands,
                                   get_source_tarball_building_commands,
                                   debian_source_transformer,
                                   source_tarball_transformer
                                   )
from .platform import GithubPlatform
from .obs import OBS
from .settings import (PACKAGE,
                       PROJECT,
                       PROJECT_CLONE_URL,
                       PROJECT_CLONE_PATH,
                       COMMITTER_NAME,
                       COMMITTER_EMAIL,
                       VERSION_FILE,
                       SOURCE_TARBALL_DOCKERFILE,
                       DEBIAN_SOURCE_DOCKERFILE,
                       PULL_REQUEST_TITLE,
                       PULL_REQUEST_BODY,
                       TZ_OFFSET,
                       DEBIAN_CHANGELOG_FILE,
                       DEBIAN_CHANGELOG,
                       SOURCE_MOUNT_DIRECTORY
                       )


class SyslogNgRelease(object):
    def __init__(self, target_branch, release_name, release_tag, version):
        self._successful = False
        self._target_branch = target_branch
        self._release_name = release_name
        self._release_tag = release_tag
        self._version = version
        # Configure logger
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        channel = logging.StreamHandler(sys.stdout)
        channel.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        channel.setFormatter(formatter)
        self._logger.addHandler(channel)

    def _setup(self):
        """
            Setup the platform client for committer information
        """
        self._platform_cli = GithubPlatform(PROJECT)
        self._platform_cli.set_committer(COMMITTER_NAME,COMMITTER_EMAIL)
        self._version_bump_msg = "autorel bumped the version to {0}".format(self._version)
        self._tag_msg = "{0} release".format(self._release_name)

    def _clone_repo(self, branch):
        """
            Clones the remote repository
        """
        self._repo = pygit2.clone_repository(url=PROJECT_CLONE_URL,
                                             path=PROJECT_CLONE_PATH,
                                             checkout_branch=branch
                                             )

    def _generate_changelog(self):
        """
            Generates the changelog
        """
        current_tag = self._platform_cli.get_current_release()
        latest_commit_sha = self._platform_cli.get_tagged_commit(current_tag)
        self._logger.debug("The last tagged commit is {0}".format(latest_commit_sha))
        changelog_gen = ChangelogGenerator(PROJECT_CLONE_PATH,
                                           latest_commit_sha
                                           )
        changelog_gen.generate()
        return changelog_gen.render()

    def _create_release_branch(self):
        """
            Create a release branch from the target branch
        """
        self._release_branch = "release_{0}".format(self._release_tag)
        self._platform_cli.create_new_branch(self._target_branch,
                                             self._release_branch
                                             )

    def _increase_version(self):
        """
            Increase the version number in the repo
        """
        version_file_path = os.path.join(PROJECT_CLONE_PATH,
                                         VERSION_FILE
                                         )
        with open(version_file_path,"w") as f:
            f.write(self._version)
        self._version_bump_commit = self._platform_cli.create_commit(self._release_branch,
                                                                     version_file_path,
                                                                     self._version_bump_msg,
                                                                     VERSION_FILE
                                                                     )

    def _edit_debian_changelog(self):
        date = datetime.datetime.now().isoformat()
        date += TZ_OFFSET
        debian_changelog_file_path = os.path.join(PROJECT_CLONE_PATH,
                                                  DEBIAN_CHANGELOG_FILE
                                                  )
        print(debian_changelog_file_path)
        debian_changelog = DEBIAN_CHANGELOG.format(PACKAGE_NAME=PACKAGE,
                                                   PACKAGE_VERSION=self._version,
                                                   RELEASE_TAG=self._release_tag,
                                                   CURRDATE=date
                                                   )
        with open(debian_changelog_file_path,"w") as f:
            f.write(debian_changelog)
        self._platform_cli.create_commit(self._release_branch,
                                         debian_changelog_file_path,
                                         self._version_bump_msg,
                                         DEBIAN_CHANGELOG_FILE
                                         )


    def _create_tag(self):
        """
            Tag the last commit using the tag_name
        """
        self._platform_cli.create_annoted_tag(self._release_tag,
                                              self._tag_msg,
                                              self._version_bump_commit,
                                              "commit"
                                              )

    def _build_distball(self,source_locaction):
        """
            Generates the distribution tarball from the source code
        """
        build_commands = get_source_tarball_building_commands(SOURCE_MOUNT_DIRECTORY)
        docker = Docker()
        source_parent_directory = os.path.abspath(os.path.dirname(source_locaction))
        return docker.run(SOURCE_TARBALL_DOCKERFILE,
                          source_parent_directory,
                          build_commands,
                          source_tarball_transformer
                          )

    def _build_debian_source(self,distball_location):
        """
            Generated the debian source package
        """
        build_commands = get_debian_source_building_commands(SOURCE_MOUNT_DIRECTORY)
        docker = Docker()
        distball_parent_directory = os.path.abspath(os.path.dirname(distball_location))
        return docker.run(DEBIAN_SOURCE_DOCKERFILE,
                          distball_parent_directory,
                          build_commands,
                          debian_source_transformer
                          )


    def _upload_to_obs(self, debian_source_package):
        """
            Uploads the repository to OBS
        """
        script_args = [
            debian_source_package.linked_tarball_path,
            debian_source_package.patch_file_path,
            debian_source_package.source_control_file_path
        ]
        # Don't hardcode it
        UPLOAD_SCRIPT = "/home/ank/test/syslog-ng-autorel/autorel/release/upload_job.py"
        os.system("python2 {0} {1}".format(UPLOAD_SCRIPT,
                                           " ".join(script_args)
                                           )
                 )

    def _send_pull_request(self):
        """
            Sends the pull request to the master branch
        """
        self._platform_cli.create_pull_request(PULL_REQUEST_TITLE,
                                               PULL_REQUEST_BODY,
                                               self._release_branch,
                                               self._target_branch
                                               )
    
    def _send_mail(self):
        """
            Sends a mail to the mailing list regarding the new release
        """
        pass

    def _create_release_draft(self, changelog_file):
        # Need a way to upload the release asset
        # Need to look into the pygithub module
        with open(changelog_file,'r') as f:
          release_message = f.read()
        self._platform_cli.create_release(self._release_tag,
                                          self._release_name,
                                          release_message,
                                          draft=True,
                                          prerelease=True
                                          )

    def release(self):
        """
            Carry out the release operation
        """
        self._logger.info("Setting up things for release")
        self._setup()
        
        # clone the master branch
        self._logger.info("Cloning target branch at {0}".format(PROJECT_CLONE_PATH))
        self._clone_repo(self._target_branch)

        # generate changelog using master
        self._logger.info("Generating the changelog")
        changelog_file = self._generate_changelog()
        self._logger.info("Changelog generated at {0}".format(changelog_file))

        # create a release branch
        self._logger.info("Creating release branch")
        self._create_release_branch()

        # increase version on the release branch
        self._logger.info("Increasing version")
        self._increase_version()
        self._edit_debian_changelog()

        # tag it
        self._logger.info("Tagging the repo")
        self._create_tag()

        # clone the release branch & delete existing branch
        self._logger.info("Cloning release branch")
        shutil.rmtree(PROJECT_CLONE_PATH)
        self._clone_repo(self._release_branch)

        # build the distribution tarball
        self._logger.info("Building the distribution tarball")
        distball_location = self._build_distball(PROJECT_CLONE_PATH)
        # copy the distball to a seperate location
        distball_directory = tempfile.mkdtemp()
        shutil.copy(distball_location,distball_directory)
        distball_location = os.path.join(distball_directory,
                                         os.path.basename(distball_location)
                                         )
        
        # build debian source
        self._logger.info("Building the debian source")
        debian_source_package = self._build_debian_source(distball_location)

        # upload to obs
        self._logger.info("Uploading to OBS")
        self._upload_to_obs(debian_source_package)

        # send pull request
        self._logger.info("Creating pull request")
        self._send_pull_request()

        # create release draft
        self._logger.info("Creating release draft")
        self._create_release_draft(changelog_file)
        self._logger.info("Release done")
