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

    def __init__(self, path, type, name=None, time_format=None, sample_length=None):
        """
        Constructor

        Args:
            path (str):             Path on disk to the document.
            type (str):             The type of page this document is. For
                                        example 'Posts', or 'Pages'.
            name (str):             The name of the document. Defaults
                                        to basename
            time_format (str):      Format string for the time.
            sample_length (str):    Word limit for sample content.
        """
        self.path = self._validate_path(path)
        self.time_format = time_format or '%m/%d/%Y'
        try:
            self.type = getattr(PageType, type.lower())
        except AttributeError:
            raise ValueError('{0} is not a valid type!'.format(type))

        self.metadata, self.raw_content = utils.parse_markdown_from_file(self.path)

        self.name = name or self.metadata.pop('name', os.path.basename(self.path).split('.')[0])
        self.title = self.metadata.pop('title', self.name)
        self.template_name = self.metadata.pop('template', '{0}.html.j2'.format(self.type))
        self.navbar = utils.str_to_bool(self.metadata.pop('navbar', 'True'))
        self.href = self.metadata.pop('href', self._generate_href())
        self.date = self._process_date(raw_date=self.metadata.pop('date', None))
        self.date_str = self._create_date_string()
        self.sample_length = sample_length if sample_length is not None else defaults.sample_length

    def __repr__(self):
        return '{0}'.format(self.path)

    def __str__(self):
        return '{0}'.format(self.path)

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

    def _munge_site_vars(self, site_vars, content, **kwargs):
        """
        This munges site vars to accomadate our various doc types. I'm
            also doing any munging that each doc type requires.

        Args:
            site_vars (dict):       The dict to munge.
            content (str):          Rendered page content.

        Returns:
            dict
        """

        site_vars['{0}_body'.format(self.type)] = content
        site_vars['{0}_summary'.format(self.type)] = self._generate_sample_content(
            content,
            sample_length=self.sample_length
        )
        site_vars['{0}_title'.format(self.type)] = self.title
        site_vars['active_page'] = 'blog' if self.type == 'post' else self.title
        if kwargs:
            site_vars.update(kwargs)

        return site_vars

    def _generate_sample_content(self, content, sample_length=50):
        """
        Generate a sample "Post".

        Args:
            content (str):      The content to create a sample of.
        """

        return ' '.join(content.split()[:sample_length])

    @abstractmethod
    def render(self, templates_path, **kwargs):
        """
        Render out a document
        """
        raise NotImplementedError()
