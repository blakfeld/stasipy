"""
document.py:
    Class for Documents (eg posts, pages, etc).

Author: Corwin Brown
Date: 05/24/2016
"""
from __future__ import absolute_import

import os

import stasipy.utils as utils


class Document(object):
    """
    Base Document class
    """

    def __init__(self, path, type):
        """
        Constructor

        Args:
            path (str):     Path on disk to the document in for this
                                document.
            type (str):     The type of document this is. For example:
                                "Posts" or "Pages"
        """
        self.path = path
        self.name = os.path.splitext(os.path.basename(self.path))[0]
        self.type = type.lower()
        self.template_name = '{0}.html.j2'.format(utils.make_singular(self.type))
        self.metadata, self.content = utils.parse_markdown(self.path)
        self.title = self.metadata.pop('title', self.name)

    def __repr__(self):
        return '{0}'.format(self.path)

    def __str__(self):
        return '{0}'.format(self.path)

    def render(self, templates_path, **kwargs):
        """
        Render Document
        """
        site_vars = self.metadata
        site_vars.update(kwargs)
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            post_title=self.title,
            post_body=self.content,
            **site_vars
        )
