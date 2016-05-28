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
    """

    def __init__(self, path, type, name=None):
        """
        Constructor

        Args:
            path (str):     Path on disk to the document.
            type (str):     The type of document this is. For example 'Posts',
                                or 'Pages'. This should probably be an ENUM.
            name (str):     The name of the document. Defaults to basename

        """
        super(self.__class__, self).__init__(path=path, type=type, name=name)
        self.template_name = '{0}.html.j2'.format(utils.make_singular(self.type))
        self.title = self.name

    def render(self, templates_path, **kwargs):
        """
        Render a jinja template file.

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
        site_vars['{0}_body'.format(self.type)] = raw_content
        site_vars['{0}_title'.format(self.type)] = self.title

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **site_vars
        )
