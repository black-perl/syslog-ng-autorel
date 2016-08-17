"""
    @module settings
    Configuration options for builders
"""
import os


## Path of the build direcory within the source ##
BUILD_DIRECTORY_SUBPATH = "build"

## Path of the docker image used for building debian source ##
DEBIAN_SOURCE_BUILDING_IMAGE = os.path.abspath("../dockerfiles/debian-source-build")

## Wildcard used fo matching the orig tarball file ##
ORIG_TARBALL_FILE_WILDCARD = "*orig.tar.gz"

## Wildcard used for matching the quilt format based patch file ##
PATCH_FILE_WIDLCARD = "*.tar.xz"

## Wildcard used for matching the source control files(.dsc) ##
SOURCE_CONTROL_FILE_WILDCARD = "*.dsc"

## Wildcard used for matching the path of the source directory ##
SOURCE_DIRECTORY_WILDCARD = "syslog-ng-*"

## Path of the docker image used for building source tarball ##
SOURCE_TARBALL_BUILDING_IMAGE = os.path.abspath("../dockerfiles/source-tarball-build")

## Wildcard used for matching the path of the source tarball ##
TARBALL_FILE_WILDCARD = "syslog-ng-*.tar.gz"

## The Source directory ##
SOURCE_DIRECTORY = "syslog-ng"

## Version ##
VERSION = "3.8.0alpha0"

## Original tarball extension ##
ORIG_TARBALL_FILE_FORMAT = "syslog-ng_{0}.orig.tar.gz"
