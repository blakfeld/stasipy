"""
markdown.py:
    Class for Markdown documents.

Author: Corwin Brown
Date: 05/28/2016
"""
from __future__ import absolute_import

import stasipy.utils as utils
from stasipy.document_types import Document


class MarkdownDocument(Document):
    """
    Implementation of the Document class for Markdown Documents.
    """

    def __init__(self, path, type, name=None, site_config=None):
        """
        Constructor

        Args:
            path (str):             Path on disk to the document.
            type (str):             The type of document this is. For example 'Posts',
                                        or 'Pages'.
            name (str):             The name of the document. Defaults to basename
            site_config (dict):     The base site config (used to render base
                                        page content.)

        """
        super(self.__class__, self).__init__(path=path,
                                             type=type,
                                             name=name,
                                             site_config=site_config)

    def render(self, templates_path, **kwargs):
        """
        Render a markdown file.

        Args:
            templates_path (str):   Path to search for templates.
            kwargs (dict):          Any additional data to push down to
                                        the template.
        """
        # Construct our variables.
        template_vars = self._build_template_vars(**kwargs)

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **template_vars
        )
