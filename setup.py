#!/usr/bin/env python

import os
from setuptools import setup


def read(fname):
    """
    Read a file and return it's raw contents.

    Args:
        fname( str):    Path of file to read.

    Returns:
        str
    """
    with open(os.path.join(os.path.dirname(__file__), fname), 'r') as f:
        return f.read()


def get_requirements():
    """
    Read requirements.txt and split it into a list.

    Returns:
        list
    """
    return read('requirements.txt').split('\n')


setup(name='stasipy',
      version='0.1',
      description='Static site generator written in Python.',
      long_description=read('README.md'),
      author='Corwin Brown',
      author_email='corwin@corwinbrown.com',
      packages=['stasipy'],
      scripts=['bin/stasipy'],
      install_requires=get_requirements(),
      platform='all')
