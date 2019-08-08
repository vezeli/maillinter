# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

__version__ = "0.4.0"

__all__ = [
    "__title__", "__summary__", "__uri__", "__author__",
    "__email__", "__license__", "__copyright__",
]

__title__ = "maillinter"
__summary__ = "maillinter helps structure the content of an e-mail"
__uri__ = "https://github.com/vezeli/maillinter"

__author__ = "Velibor Zeli"
__email__ = "zeli.velibor@gmail.com"

__license__ = "MIT"
__copyright__ = "Copyright 2019 {}".format(__author__)

_loc_version = None


def get_local_version():
    """Get a long "local" version."""

    global _loc_version

    if _loc_version is None:
        from setuptools_scm import get_version

        try:
            _loc_version = get_version(root="../..", relative_to=__file__)
        except (LookupError, AssertionError):
            _loc_version = __version__

    return _loc_version
