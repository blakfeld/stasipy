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

    def __init__(self, path, type, name=None, time_format=None, sample_length=40):
        """
        Constructor

        Args:
            path (str):         Path on disk to the document.
            type (str):         The type of page this document is. For example
                                    'Posts', or 'Pages'.
            name (str):         The name of the document. Defaults to basename
            site_vars (dict):   Variables to render into the templated
                                    Document.
            time_format (str):  The time format to use.
        """
        super(self.__class__, self).__init__(path=path,
                                             type=type,
                                             name=name,
                                             time_format=time_format,
                                             sample_length=sample_length)

    def render(self, templates_path, **kwargs):
        """
        Render an HTML file.

        Args:
            templates_path (str):       Path to search for templates.
            kwargs (dict):              Any additonal data to push down
                                            to the template.
        """
        # Construct our variables
        site_vars = kwargs

        # Read the file to get it's raw contents.
        with open(self.path, 'r') as f:
            raw_content = f.read()

        # Munch the site_vars a bit to accomodate doc_types.
        self._munge_site_vars(site_vars, raw_content)

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **site_vars
        )
