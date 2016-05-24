"""
post.py:
    Class to represent a post.

Author: Corwin Brown
Date: 05/24/2016
"""
from __future__ import absolute_import

from stasipy.document_types import DocumentType


class Post(DocumentType):
    """
    Post Document Class
    """

    def __init__(self, document_path):
        """
        Constructor

        Args:
            document_path (str):    Path on disk to the document in for
                                        this Post.
        """
        super(self.__class__, self).__init__(document_path=document_path)

    def render(**kwargs):
        """
        """
        self.metadata
        pass
