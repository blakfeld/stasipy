"""
html.py:
    Class for HTML documents.

Author: Corwin Brown
Date: 05/28/2016
"""
from __future__ import absolute_import

import stasipy.utils as utils
from stasipy.document_types import Document


class HTMLDocument(Document):
    """
    Implementation of the Document class for HTML Documents.

    Since HTML is valid markdown, I'm going to run this through a markdown
        parser, so I can continue to get metadata from each document
        without having to write my own parser.
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
        Render an HTML file.

        Args:
            templates_path (str):       Path to search for templates.
            kwargs (dict):              Any additonal data to push down
                                            to the template.
        """
        # Read the file to get it's raw contents.
        with open(self.path, 'r') as f:
            self.content = f.read()

        # Munch the site_vars a bit to accomodate doc_types.
        template_vars = self.template_vars(**kwargs)

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **template_vars
        )
