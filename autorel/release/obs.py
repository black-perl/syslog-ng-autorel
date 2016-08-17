"""
    @module obs
    @class OBS
    - Serves as OpenSuse Build Service(build.opensuse.org)
      client
"""
import os
import shutil
import tempfile
from osc.conf import (get_config,
                      write_initial_config,
                      config
                      )
from osc.core import (checkout_package,
                      Package
                      )


class OBS(object):
    """
        Expose API to do the following operations
        - checkout
        - add
        - remove
        - commit
    """
    def __init__(self, obs_project, obs_package):
        self._project_directory = tempfile.mkdtemp()
        self._obs_project = obs_project
        self._obs_package = obs_package
        self._package_directory = os.path.join(self._project_directory,
                                               self._obs_package
                                               )
        self._do_config()
        self._init_package()

    def _do_config(self):
        # write the initial config
        write_initial_config(OSC_CONFIG_FILE,
                             {
                                "user":OBS_USER,
                                "pass":OBS_PASS
                             })
        # load the config
        get_config(override_conffile=OSC_CONFIG_FILE)
        self._config = config

    def _init_package(self):
        apiurl = self._config["apiurl"]
        checkout_package(apiurl,
                         self._obs_project,
                         self._obs_package,
                         prj_dir=self._project_directory
                         )
        self._package = Package(self._package_directory)

    def add_files(self, files):
        for file_ in files:
            # file_ should be an absolute path
            shutil.copy(file_,self._package_directory)
            file_name = os.path.basename(file_)
            self._package.addfile(file_name)

    def commit(self, commit_msg):
        self._package.commit(commit_msg)

    def list_files(self):
        return self._package.filelist

    def remove_files(self, files):
        for file_ in files:
            self._package.delete_file(file_)
