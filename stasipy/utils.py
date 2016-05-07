"""
utils.py:
    Misc utility functions for Stasipy.

Author: Corwin Brown
Date: 05/01/2016
"""
from __future__ import absolute_import

import os

from stasipy.errors import StasipyException


def get_file_path(fname=None):
    """
    Get the full path to a file.

    Args:
        fname (str):    Name of the file to get. Defaults to '__file__'.
    """
    if fname is None:
        fname = __file__

    return os.path.dirname(os.path.abspath(fname))


def file_exists(fpath, specific_permission=None):
    """
    Check if a specified file path exists, and is readable.

    Args:
        fpath (str):                The path to check.
        specific_permission (int):  By default we ensure read, if this is
                                        specified, also check another
                                        permission.
    """
    if os.path.exists(fpath) and os.access(fpath, os.R_OK):
        if specific_permission is not None:
            if os.access(fpath, specific_permission):
                return True
        else:
            return True

    return False


def ensure_directory_exists(fpath):
    """
    Ensure a directory exists and is traversable.

    Args:
        fpath (str):        The path to the directory to ensure.
    """
    if not file_exists(fpath):
        os.makedirs(fpath)

    if file_exists(fpath) and not os.access(fpath, os.X_OK):
        raise StasipyException('"{0}" exists, but is not traversable!'.format(fpath))


def touch(fpath, times=None):
    """
    Python implementation of 'touch'.

    Args:
        fpath (str):    The path to touch.
        times (tuple):  A 2-tuple of numbers, of the form (atime, mtime)
                            which is used to set the access and modified
                            times.
    """
    with open(fpath, 'a'):
        os.utime(fpath, times)
