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

    def __init__(self, path, type, name=None, time_format=None, sample_length=40):
        """
        Constructor

        Args:
            path (str):     Path on disk to the document.
            type (str):     The type of document this is. For example 'Posts',
                                or 'Pages'.
            name (str):     The name of the document. Defaults to basename
            time_format (str):  The time format to use.

        """
        super(self.__class__, self).__init__(path=path,
                                             type=type,
                                             name=name,
                                             time_format=time_format,
                                             sample_length=sample_length)

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
        self._munge_site_vars(site_vars, content)

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **site_vars
        )
