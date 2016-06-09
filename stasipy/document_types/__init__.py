"""
document_types:
    Classes for the various supported document types.

Author: Corwin Brown
Date: 05/24/2016
"""
from __future__ import absolute_import

import os
from datetime import datetime
from abc import ABCMeta, abstractmethod

import stasipy.utils as utils
from stasipy.defaults import StasipyDefaults as defaults


class PageType(object):
    """
    ENUMish thing to represent the page types I'm allowing.
    """

    post = 'post'
    page = 'page'
    meta = 'meta'


class Document(object):
    """
    Base Document type class
    """

    __metaclass__ = ABCMeta

    def __init__(self, path, type, name=None, site_config=None):
        """
        Constructor

        Args:
            path (str):             Path on disk to the document.
            type (str):             The type of page this document is. For
                                        example 'Posts', or 'Pages'.
            name (str):             The name of the document. Defaults
                                        to basename
            time_format (str):      Format string for the time.
            summary_length (str):    Word limit for sample content.
        """
        self.path = self._validate_path(path)
        self.site_config = site_config or {}
        self.time_format = self.site_config.get('time_format', '%m/%d/%Y')
        try:
            self.type = getattr(PageType, type.lower())
        except AttributeError:
            raise ValueError('{0} is not a valid type!'.format(type))

        self.metadata, _ = utils.parse_markdown_from_file(self.path)

        # The Great Metadata-palooza!
        self.name = name or self.metadata.pop('name', os.path.basename(self.path).split('.')[0])
        self.title = self.metadata.pop('title', self.name)
        self.author = self.metadata.pop('author', site_config.get('maintainer', None))
        self.author_email = self.metadata.pop('author_email', site_config.get('maintainer_email', None))
        self.template_name = self.metadata.pop('template', '{0}.html.j2'.format(self.type))
        self.navbar = utils.str_to_bool(self.metadata.pop('navbar', 'True'))
        self.href = self.metadata.pop('href', self._generate_href())
        self.date = self._process_date(raw_date=self.metadata.pop('date', None))
        self.date_str = self._create_date_string()
        self.summary_length = self.site_config.get('summary_length', defaults.summary_length)

        if self.type == PageType.post:
            self.summary = self._generate_summary()
        else:
            self.summary = None

        self.content = self._render_base()

    def _process_date(self, raw_date=None):
        """
        Take a raw_date string, and parse it into a datetime object. If a
            raw_date string is not supplied, use the create time of the
            document. This is very likely not what I want, but its better
            than nothing.

        Args:
            raw_date (str):         A raw string date.

        Returns:
            datetime obj
        """
        if raw_date is not None:
            return datetime.strptime(raw_date, self.time_format)
        else:
            # Get file create date (Probably not what the user wants, but its something.)
            create_time = os.stat(self.path).st_ctime
            return datetime.fromtimestamp(create_time)

    def _create_date_string(self):
        """
        Give me a string version of this documents datetime object.

        Returns:
            str
        """
        return self.date.strftime(self.time_format)

    def _generate_href(self):
        """
        Generate a default href for the page type.
        """

        if self.type == 'meta':
            return '/{0}.html'.format(self.name)
        else:
            return '/{0}/{1}.html'.format(self.type, self.name)

    def _validate_path(self, path):
        """
        Ensure a path exists and is readable.

        Args:
            path (str):     Path to validate.

        Returns:
            str
        """
        if not utils.file_exists(path):
            raise ValueError('Nothing readable exists at "{0}"!'.format(path))
        return path

    def _build_template_vars(self, **kwargs):
        """
        Construct a dict to get passed down to our template containing
            various variables (That'd be a good band name).

        Args:
            kwargs (dict):  Whatever you'd like passed into the dict.

        Returns:
            dict
        """
        template_vars = {
            'document': self.__dict__,
            'active_page': 'blog' if self.type == 'post' else self.title,
        }
        template_vars.update(self.metadata)
        template_vars.update(self.site_config)
        template_vars.update(kwargs)

        return template_vars

    def _generate_summary(self, summary_length=50):
        """
        Generate a post summary.

        Not an ideal solution as it will eat new lines.
        """
        with open(self.path, 'r') as f:
            content = utils.remove_markdown_metadata(f.read())

        template_vars = self._build_template_vars()
        summary_content = '{0}...'.format(' '.join(content.split()[:summary_length]))
        summary_content = utils.render_template_from_string(summary_content, **template_vars)
        _, summary_content = utils.parse_markdown(summary_content)

        return summary_content

    def _render_base(self):
        """
        Render out the base "raw" content.

        Returns:
            str
        """
        template_vars = self._build_template_vars()
        _, raw_content = utils.parse_markdown_template(self.path, **template_vars)

        return raw_content

    @abstractmethod
    def render(self, templates_path, **kwargs):
        """
        Render out a document
        """
        raise NotImplementedError()
