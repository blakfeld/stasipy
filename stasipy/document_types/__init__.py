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


class DocumentType(object):
    """
    Base Document type class
    """

    __metaclass__ = ABCMeta
    _document_type = None

    def __init__(self, document_path):
        """
        Constructor

        Args:
            document_path (str):    Path on disk to the document in for
                                        this document.
        """
        self.document_path = document_path
        self.document_name = os.path.basename(self.document_path)
        self.metadata, self.content = utils.parse_markdown(self.document_path)

    @property
    def document_path(self):
        return self.document_path

    @property
    def document_type(self):
        if self._document_type is None:
            raise NotImplementedError()
        return self._document_type

    @abstractmethod
    def render(self, output_file=None):
        """
        Render out a document
        """
        raise NotImplementedError()
