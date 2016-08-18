"""
    @module utils
    Helper functions and classes used for building
    source tarballs and debian source packages
"""
import os
import glob
from build_helpers.settings import (ORIG_TARBALL_FILE_WILDCARD,
                                    PATCH_FILE_WIDLCARD,
                                    SOURCE_CONTROL_FILE_WILDCARD,
                                    SOURCE_DIRECTORY_WILDCARD,
                                    TARBALL_FILE_WILDCARD,
                                    BUILD_DIRECTORY_SUBPATH,
                                    SOURCE_DIRECTORY,
                                    ORIG_TARBALL_FILE_FORMAT,
                                    VERSION
                                    )


class DebianSourcePackage(object):
    """
        Debian source package abstraction
    """
    def __init__(self, linked_tarball, patch_file, source_control_file):
        self._linked_tarball = linked_tarball
        self._patch_file = patch_file
        self._source_control_file = source_control_file

    @property
    def linked_tarball_path(self):
        return self._linked_tarball

    @property
    def patch_file_path(self):
        return self._patch_file

    @property
    def source_control_file_path(self):
        return self._source_control_file


def get_debian_source_building_commands(input_directory):
    """
        Returns the list of commands to be executed to
        build the debian source package
    """
    orig_tarball_name = ORIG_TARBALL_FILE_FORMAT.format(VERSION)
    commands = [
        "(cd {0} && tar -xvf {1})".format(input_directory,
                                          TARBALL_FILE_WILDCARD
                                          ),
        "(cd {0} && mv {1} {2})".format(input_directory,
                                       TARBALL_FILE_WILDCARD,
                                       orig_tarball_name
                                       ),
        "(cd {0} && dpkg-source -Us -Uc -b {1})".format(input_directory,
                                                       SOURCE_DIRECTORY_WILDCARD
                                                       )
    ]
    return commands


def get_source_tarball_building_commands(input_directory):
    """
        Returns the list of commands to be executed to
        build the distribution tarball
    """
    source_location = os.path.join(input_directory,
                                   SOURCE_DIRECTORY
                                   )
    commands = [
            "(cd {0} && pip install -r requirements.txt)",
            "(cd {0} && ./autogen.sh)",
            "(cd {0} && mkdir build)",
            "(cd {0}/build && ../configure --enable-debug)",
            "(cd {0}/build && make distcheck)"
    ]
    for index in range(len(commands)):
        commands[index] = commands[index].format(source_location)
    return commands


def debian_source_transformer(input_directory):
    """
        Returns a DebianSourcePackage instance
    """
    lookup_directory = input_directory
    os.chdir(lookup_directory)
    linked_tarball = glob.glob(ORIG_TARBALL_FILE_WILDCARD)[0]
    linked_tarball = os.path.abspath(linked_tarball)
    patch_file = glob.glob(PATCH_FILE_WIDLCARD)[0]
    patch_file = os.path.abspath(patch_file)
    source_control_file = glob.glob(SOURCE_CONTROL_FILE_WILDCARD)[0]
    source_control_file = os.path.abspath(source_control_file)
    source_package = DebianSourcePackage(linked_tarball,
                                         patch_file,
                                         source_control_file
                                         )
    return source_package


def source_tarball_transformer(input_directory):
    """
        Returns the path of source tarball by looking into
        the input_directory
    """
    lookup_directory = os.path.join(input_directory,
                                    SOURCE_DIRECTORY,
                                    BUILD_DIRECTORY_SUBPATH
                                    )
    os.chdir(lookup_directory)
    distribution_tarball = glob.glob(TARBALL_FILE_WILDCARD)[0]
    distribution_tarball_path = os.path.abspath(distribution_tarball)
    return distribution_tarball_path
