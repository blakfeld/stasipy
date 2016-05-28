"""
utils.py:
    Misc utility functions for Stasipy.

Author: Corwin Brown
Date: 05/01/2016
"""
from __future__ import absolute_import, print_function

import os
import sys
import shutil

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


def ensure_directory_absent(fpath):
    """
    Ensure that a directory does NOT exist.

    Args:
        fpath (str):        The path of the directory to ensure absent.
    """
    if file_exists(fpath):
        if os.path.isdir(fpath):
            shutil.rmtree(fpath)
        else:
            os.remove(fpath)


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


def parse_markdown_from_file(fpath):
    """
    Parse a markdown file.

    Args:
        fpath (str):        The path of the file to parse.

    Returns:
        Tuple:              (metadata, content)
    """
    if not file_exists(fpath):
        raise ValueError('Unable to read file at location: {0}'.format(fpath))
    with open(fpath, 'r') as f:
        metadata, content = parse_markdown(f.read())

    return metadata, content


def parse_markdown_template(fpath, **kwargs):
    """
    Parse a markdown file, but treat it like a JINJA2 template.

    Args:
        fpath (str):        The path of the file to parse.

    Returns:
        Tuple:              (metadata, content)
    """
    if not file_exists(fpath):
        raise ValueError('Unable to read file at location: {0}'.format(fpath))
    with open(fpath, 'r') as f:
        fpath_contents = f.read()

    # Get the document metadata, so it can appear in the content.
    metadata, _ = parse_markdown(fpath_contents)

    # Update our kwargs with the metadata
    kwargs.update(metadata)

    # Template, and render the templated markdown
    templated_content = render_template_from_string(fpath_contents, **kwargs)
    _, content = parse_markdown(templated_content)

    return metadata, content


def parse_markdown(md_content):
    """
    Parse a markdown string into HTML.

    Args:
        markdown (str):     Markdown content to parse.

    Returns:
        Tuple:              (metadata, content)
    """
    content = markdown(md_content, extras=['metadata'])
    metadata = content.metadata

    return metadata, content


def render_template_from_file(templates_path, template_name, **kwargs):
    """
    Render a JINJA template from a file.

    Args:
        templates_path (str):   The search path for templates.
        template_name (str):    The template to render.
        kwargs (dict):          Any other variables you wish to render into
                                    the template.

    Returns:
        str (Rendered Template)
    """
    env = j2.Environment(loader=j2.FileSystemLoader(templates_path))
    template = env.get_template(template_name)
    return template.render(kwargs)


def render_template_from_string(template_string, **kwargs):
    """
    Render a template from a string.

    Args:
        template_string (str):      The template to use.
        kwargs (dict):              Any other variables you wish to render
                                        into the template.

    Returns:
        str (Rendered Template)
    """
    env = j2.Environment()
    template = env.from_string(template_string)
    return template.render(kwargs)


def str_to_bool(s):
    """
    Convert a string to a boolean.

    Args:
        s (str):    String to convert.
    """
    if s.lower() == 'true':
        return True
    else:
        return False

def print_err(*args, **kwargs):
    """
    Print to stderr

    Args:
        *args to pass down to print function.
        *kwargs to pass down to print function.
    """
    print(*args, file=sys.stderr, **kwargs)
