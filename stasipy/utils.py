"""
utils.py:
    Misc utility functions for Stasipy.

Author: Corwin Brown
Date: 05/01/2016
"""
from __future__ import absolute_import

import os

import jinja2 as j2
from markdown2 import markdown

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


def list_files(path):
    """
    Generator to Emulate something like:
        find ./ -f

    This will blow apart a directory tree and allow me to easily
        search for a file. Since this is a generator, it should
        be mitigate a lot of the ineffiency of walking the whold
        directory.

    Args:
        path (str): The path to traverse.

    Returns:
        str: files in the path.
    """
    for root, folders, files in os.walk(path):
        for filename in folders + files:
            yield os.path.join(root, filename)


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


def confirm_dialog(msg, default=None):
    """
    Display a "yes/no" confirm dialog to the user.

    Args:
        msg (str):      The prompt to show the user.
        default (str):  The default answer.
    """
    msg = '{0} [y|n]'.format(msg)
    if default is not None:
        if default.lower() not in ['y', 'yes', 'n', 'no']:
            raise ValueError('"{0}" is not a valid default value for "confirm_dialog".'
                             .format(default))
        msg = '{0} (default: {1})'.format(msg, default)

    prompt = '{0}: '.format(msg)
    while True:
        confirm = raw_input(prompt).lower()
        if not confirm and default is not None:
            confirm = default.lower()

        if confirm == 'y' or confirm == 'yes':
            return True
        elif confirm == 'n' or confirm == 'no':
            return False
        else:
            print('Please enter y (yes) or n (no).\n')


def make_singular(s):
    """
    Take a string, and chop the S off the end of it. This is not smart enough
        to determine if a word should end in "s" or not, so... yeah.

    Args:
        s (str):        The string to truncate an S off of.
    """
    if s.endswith('s'):
        return s[:-1]
    else:
        return s


def parse_markdown(document):
    """
    Parse a markdown document, and return a tuple of (metadata, content)

    Args:
        document (str):     The path to the document you wish to parse.

    Returns:
        Tuple:              (metadata, content)
    """
    if not file_exists(document):
        raise ValueError('Unable to read document at location: {0}'.format(document))

    with open(document, 'r') as f:
        content = markdown(f.read(), extras=['metadata'])

    metadata = content.metadata

    return metadata, content


def render_template_from_file(templates_path, template_name, **kwargs):
    env = j2.Environment(loader=j2.FileSystemLoader(templates_path))
    template = env.get_template(template_name)
    return template.render(kwargs)
