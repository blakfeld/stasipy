"""
template.py:
    Class for Template documents.

Author: Corwin Brown
Date: 05/28/2016
"""
from __future__ import absolute_import

import stasipy.utils as utils
from stasipy.document_types import Document


class TemplateDocument(Document):
    """
    Implementation of the Document class for Template Documents.

    Given the context of a webpage, I'm abusing the fact that HTML is
        technically valid markdown. So I'm assuming you've very likely
        handed me a document that contains HTML with jinja templating.
        This allows me to get all the same metadata I would get from a
        markdown page without having to write the parser myself.
    """

    def __init__(self, path, type, name=None, time_format=None, sample_length=40):
        """
        Constructor

        Args:
            path (str):     Path on disk to the document.
            type (str):     The type of document this is. For example 'Posts',
                                or 'Pages'. This should probably be an ENUM.
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
        Render a jinja template file.

        Args:
            templates_path (str):       Path to search for templates.
            kwargs (dict):              Any additonal data to push down
                                            to the template.
        """
        # Construct our variables
        site_vars = kwargs

        # Blow out the template.
        _, content = utils.parse_markdown_template(self.path, **site_vars)

        # Munch the site_vars a bit to accomadate doc_types.
        self._munge_site_vars(site_vars, content)

        # Render the page.
        return utils.render_template_from_file(
            templates_path=templates_path,
            template_name=self.template_name,
            **site_vars
        )
