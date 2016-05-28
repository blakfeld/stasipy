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
        self.metadata, self.raw_content = utils.parse_markdown_from_file(self.path)
        self.title = self.metadata.pop('title', self.name)

    def render(self, templates_path, **kwargs):
        """
        Render a markdown file.

        Args:
            templates_path (str):   Path to search for templates.
            kwargs (dict):          Any additional data to push down to
                                        the template.
        """
        # Construct our variables.
        site_vars = self.metadata
        site_vars.update(kwargs)

        # Ensure any templates in the markdown are blown out.
        _, content = utils.parse_markdown_template(self.path, **site_vars)

        # Munge the site_vars a bit to accomodate doc_types.
        site_vars['{0}_body'.format(self.type)] = content
        site_vars['{0}_title'.format(self.type)] = self.title

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **site_vars
        )
