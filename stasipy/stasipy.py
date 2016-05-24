"""
stasipy.py:
    Class that contains most of the Stasipy business logic.

Author: Corwin Brown
Date: 05/07/2016
"""
from __future__ import absolute_import

import os
import yaml
import shutil
import pkg_resources

import stasipy.utils as utils
from stasipy.document import Document
from stasipy.errors import StasipyException
from stasipy.defaults import StasipyDefaults


class Stasipy(object):
    """
    Main Stasipy Class.
    """

    template_site_name = 'template_site'

    # This is the document types were supporting. So these are the
    #   templates/documents we'll search "src" for.
    # TODO: This should be dynamically figured out based upon
    #   the directories in "src", or at the very least configurable
    #   within a site config.
    supported_document_types = [
        'posts',
        'pages',
    ]

    def __init__(self, base_site_path, site_name=None, verbose_mode=None, skip_confirm=False):
        """
        Constructor.

        Args:
            base_site_path (str):       Path to where the site/project is on
                                            disk.
            site_name (str):            Name of the site.
            config_path (str):          Path to the site config file.
            verbose_mode (bool):        Toggle verbose mode.
            skip_confirm (bool):        Skip any confirmation dialogs.
        """

        base_site_path = os.path.expanduser(base_site_path)
        if site_name is not None:
            self.base_site_path = os.path.join(base_site_path, site_name)
        else:
            self.base_site_path = base_site_path

        # Source Paths.
        self.source_path = os.path.join(self.base_site_path, 'src')
        self.source_posts_path = os.path.join(self.source_path, 'posts')
        self.source_pages_path = os.path.join(self.source_path, 'pages')

        # Staging Paths.
        self.staging_path = os.path.join(self.base_site_path, '.out.staging')
        self.posts_staging_path = os.path.join(self.staging_path, 'posts')
        self.pages_staging_path = os.path.join(self.staging_path, 'pages')

        # Output Paths.
        self.out_path = os.path.join(self.base_site_path, 'out')

        self.templates_path = os.path.join(self.source_path, 'templates')
        self.site_name = site_name or self._site_name_from_path(self.base_site_path)
        self.verbose_mode = True if verbose_mode else False
        self.site_structure = StasipyDefaults.default_site_structure
        self.skip_confirm = skip_confirm
        self.site_vars = None

    def __del__(self):
        """
        Destructor.
        """

        self._clean()

    def _site_name_from_path(self, path):
        """
        Try and resovle a site_name from a file path.

        We'll do this by splitting a file path, reversing it
            and taking the first thing that isn't an empty
            string.

        Args:
            path (str):     The path to parse.

        Returns:
            str
        """
        split_path = path.split(os.sep)
        split_path.reverse()
        for part in split_path:
            if part != '':
                return part
        return None

    def init(self):
        """
        Intialize a Base Site.
        """
        self._verbose('Initializing site: "{0}"'.format(self.site_name))

        if utils.file_exists(self.base_site_path):
            overwrite = self._confirm_dialog(
                msg='Something exists at "{0}"! Overwrite?'.format(self.base_site_path),
                default='n'
            )
            if overwrite:
                shutil.rmtree(self.base_site_path)
            else:
                return

        self._verbose('Copying template site to: {0}'.format(self.base_site_path))
        template_site_path = pkg_resources.resource_filename(__name__, self.template_site_name)
        shutil.copytree(template_site_path, self.base_site_path)

        self._verbose('Generating initial "siteconfig.yml" file.')
        self._generate_base_site_config()

    def _generate_base_site_config(self, **kwargs):
        """
        Generate an initial config file.

        Args:
            site_name (str):        The name of your site. This will be the
                                        top level key in your config.
            **kwargs (dict):        Whatever is supplied will be fed into
                                        the config file.
        """
        config_data = StasipyDefaults.default_site_config
        config_data['site_name'] = self.site_name
        config_data.update(kwargs)
        config_path = os.path.join(self.base_site_path, 'siteconfig.yml')
        with open(config_path, 'w') as f:
            f.write('---\n')
            f.write(yaml.dump(config_data, default_flow_style=False))

    def generate(self):
        """
        Generate a new site from source.
        """
        # Get data from site_config
        self.site_vars = self._read_site_config()

        # Ensure the source path exists.
        if not utils.file_exists(self.source_path):
            raise StasipyException('Source path does not exists at: "{0}"'.format(self.source_path))

        # Find our posts and pages.
        self._verbose('Discovering posts.')
        posts = self._discover_documents(self.source_posts_path, 'post')

        self._verbose('Discovering pages.')
        pages = self._discover_documents(self.source_pages_path, 'page')
        if posts or pages:
            self._verbose('Discovered documents!\nPosts:\n\t- {0}\nPages: \n\t- {1}'.format(
                          '\n\t- '.join([str(p) for p in posts] if posts else ''),
                          '\n\t- '.join([str(p) for p in pages]) if pages else ''))
        else:
            utils.print_err('No documents found!')
            return 1

        # Render out our posts/pages
        self._verbose('Rendering posts.')
        rendered_posts = {p.name: self._render_document(p) for p in posts}

        self._verbose('Rendering pages.')
        rendered_pages = {p.name: self._render_document(p) for p in pages}

        # Generate the "out" staging directory.
        try:
            self._create_staging_out_dir()
        except ValueError as e:
            utils.print_err('Error: {0}'.format(e))
            return 1

        # Write the rendered posts/pages.
        self._verbose('Writing out posts.')
        self._write_documents(rendered_posts, self.posts_staging_path)

        self._verbose('Writing out pages.')
        self._write_documents(rendered_pages, self.pages_staging_path)

        # Finalize the site.
        self._finalize_site()

    def _finalize_site(self):
        """
        Copy staging over to production.
        """
        if not os.path.exists(self.staging_path):
            raise ValueError('Staging path does not exist at: "{0}"'.format(self.staging_path))

        # If our 'out' path exists, remove it, so we can create a new one.
        if os.path.exists(self.out_path):
            shutil.rmtree(self.out_path)

        # Copy over our "staging" site.
        shutil.copytree(self.staging_path, self.out_path)

    def _create_staging_out_dir(self):
        """
        Create a staging out directory, so we can generate all of our content
            with minimal interupption of the site.

        Args:
            output_staging_path (str):      The path to create the staging dir.

        Raises:
            ValueError when staging directory already exists, and 'n' is
                selected at the overwrite prompt.
        """
        if utils.file_exists(self.staging_path):
            delete_old_staging = self._confirm_dialog(
                'Staging directory already exists at "{0}"! Overwrite?'.format(self.staging_path),
                default='n',
            )
            if delete_old_staging:
                shutil.rmtree(self.staging_path)
            else:
                raise ValueError('Staging directory "{0}" already exists!')
        utils.ensure_directory_exists(self.staging_path)
        utils.ensure_directory_exists(self.posts_staging_path)
        utils.ensure_directory_exists(self.pages_staging_path)

    def _read_site_config(self):
        """
        Read the config for a site, and return it's contents as
            a dict.

        Returns:
            dict
        """
        site_config_data = {}
        site_config_path = os.path.join(self.base_site_path, 'siteconfig.yml')
        if utils.file_exists(site_config_path):
            with open(site_config_path, 'r') as f:
                site_config_data = yaml.load(f.read())

        return site_config_data

    def _render_document(self, document):
        """
        Render out a document, keeping any data I might want later
            intact.

        Args:
            document (document obj):    Document object to render.

        Returns:
            dict
        """
        rendered_document = {
            'title': document.title,
            'metadata': document.metadata,
            'content': document.render(self.templates_path, **self.site_vars),
        }

        return rendered_document

    def _write_documents(self, rendered_documents, output_path):
        """
        Write out a rendered document.
        """
        for name, attrs in rendered_documents.items():
            document_output_path = os.path.join(output_path, '{0}.html'.format(name))
            with open(document_output_path, 'w') as f:
                f.write(attrs['content'])

    def _discover_documents(self, path_to_search, document_type):
        """
        Search a directory for documents.

        Args:
            path_to_search (str):       The root directory to search in.
            document_type (str):        The type of document I'm searching for.
        """
        # Find Markdown files and create a Document object.
        documents = []
        for fpath in utils.list_files(path_to_search):
            fname, fext = os.path.splitext(fpath)
            if not fext == '.md':
                continue
            doc = Document(path=os.path.join(path_to_search, fpath),
                           type=document_type)
            documents.append(doc)

        return documents

    def serve(self):
        """
        Serve the site.
        """
        pass

    def _verbose(self, msg):
        """
        If verbose mode is true, output a msg.
        """
        # Don't print an empty message, and bomb if verbose is falsey.
        if not self.verbose_mode or not msg:
            return

        print msg

    def _confirm_dialog(self, msg, default='n'):
        """
        Wraps the "confirm_dialog" method in utils to avoid
            checking for the "skip_confirm" option each time.

        Args:
            msg (str):      The prompt to show the user.
            default (str):  The default option.

        Returns:
            bool
        """
        if self.skip_confirm:
            return True
        else:
            return utils.confirm_dialog(msg, default=default)

    def _clean(self):
        """
        Clean up any files that may have been created.
        """
        utils.ensure_directory_absent(self.staging_path)
