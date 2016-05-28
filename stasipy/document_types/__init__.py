"""
document_types:
    Classes for the various supported document types.

Author: Corwin Brown
Date: 05/24/2016
"""
from __future__ import absolute_import

import os
from abc import ABCMeta, abstractmethod

import stasipy.utils as utils


class PageType(object):
    """
    ENUMish thing to represent the page types I'm allowing.
    """

    post = 'post'
    page = 'page'


class Document(object):
    """
    Base Document type class
    """

    __metaclass__ = ABCMeta

    def __init__(self, path, type, name=None):
        """
        Constructor

        Args:
            path (str):     Path on disk to the document.
            type (str):     The type of page this document is. For example
                                'Posts', or 'Pages'.
            name (str):     The name of the document. Defaults to basename
                                of the path.
        """
        self.path = self._validate_path(path)
        self.name = name or os.path.splitext(os.path.basename(self.path))[0]
        try:
            self.type = getattr(PageType, type.lower())
        except AttributeError:
            raise ValueError('{0} is not a valid type!'.format(type))

    def __repr__(self):
        return '{0}'.format(self.path)

    def __str__(self):
        return '{0}'.format(self.path)

    def _validate_path(self, path):
        """
        Ensure a path exists and is readable.

        Args:
            path (str):     Path to validate.

        Returns:
            str
        """
        if not utils.file_exists(path):
            raise ValueError('Nothing readable exists at "{0}"!'.format(path))
        return path

    @abstractmethod
    def render(self, output_file=None):
        """
        Render out a document
        """
        raise NotImplementedError()
