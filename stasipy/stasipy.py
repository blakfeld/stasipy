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

import markdown2 as markdown

import stasipy.utils as utils
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

    def __init__(self, base_site_path, site_name=None, verbose_mode=None):
        """
        Constructor.

        Args:
            base_site_path (str):       Path to where the site/project is on
                                            disk.
            site_name (str):            Name of the site.
            config_path (str):          Path to the site config file.
            verbose_mode (bool):        Toggle verbose mode.
        """

        base_site_path = os.path.expanduser(base_site_path)
        if site_name is not None:
            self.base_site_path = os.path.join(base_site_path, site_name)
        else:
            self.base_site_path = base_site_path

        self.site_name = site_name or os.path.basename(base_site_path)
        self.verbose_mode = True if verbose_mode else False
        self.site_structure = StasipyDefaults.default_site_structure

    def init(self):
        """
        Intialize a Base Site.
        """
        self._verbose('Initializing site: "{0}"'.format(self.site_name))

        if utils.file_exists(self.base_site_path):
            overwrite = utils.confirm_dialog(
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
        self._generate_base_site_config(site_name=self.site_name)

    def _generate_base_site_config(self, site_name, **kwargs):
        """
        Generate an initial config file.

        Args:
            site_name (str):        The name of your site. This will be the
                                        top level key in your config.
            **kwargs (dict):        Whatever is supplied will be fed into
                                        the config file.
        """
        config_data = {
            site_name: StasipyDefaults.default_site_config
        }
        config_data[site_name].update(kwargs)

        config_path = os.path.join(self.base_site_path, 'siteconfig.yml')

        with open(config_path, 'w') as f:
            f.write('---\n')
            f.write(yaml.dump(config_data, default_flow_style=False))

    def generate(self):
        """
        Generate a new site from source.
        """
        source_path = os.path.join(self.base_site_path, 'src')
        if not utils.file_exists(source_path):
            raise StasipyException('Source path does not exists at: "{0}"'.format(source_path))

        all_docs = self._discover_documents(source_path, self.supported_document_types)
        self._verbose('Discovered documents:\n{0}'.format(yaml.dump(all_docs, default_flow_style=False)))

        output_path = os.path.join(self.base_site_path, 'out')
        if utils.file_exists(output_path):
            backup_path = os.path.join(self.base_site_path, 'out.backup')
            if utils.file_exists(backup_path):
                delete_backup = utils.confirm_dialog(
                    'Backup "out" directory already exists at "{0}". Overwrite?'.format(backup_path),
                    default='n'
                )
                if delete_backup:
                    shutil.rmtree(backup_path)
                else:
                    return
            shutil.copytree(output_path, backup_path)
        utils.ensure_directory_exists(output_path)

        for doc_type, docs in all_docs.items():
            doc_type_path = os.path.join(output_path, doc_type)
            utils.ensure_directory_exists(doc_type_path)
            for doc in docs:
                metadata, content = utils.parse_markdown(doc)
                print 'metadata: {0}'.format(metadata)
                print 'content: {0}'.format(content)

    def _discover_documents(self, source_path, doc_types):
        """
        Discover any documents of a specified type.

        Args:
            source_path (str):      The path to search.
            doc_types (str):        The document types to search for.

        Returns:
            dict
        """
        docs = {}
        for doc_type in doc_types:
            doc_path = os.path.join(source_path, doc_type)
            docs[doc_type] = self._discover_markdown_files(doc_path)

        return docs

    def _discover_markdown_files(self, path_to_search):
        """
        Search a directory for markdown files.

        Args:
            path_to_search (str):       The root directory to search in.
        """
        markdown_files = []
        for fpath in utils.list_files(path_to_search):
            if fpath.endswith('.md'):
                markdown_files.append(fpath)

        return markdown_files

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

if __name__ == '__main__':
    new_site = Stasipy(os.path.expanduser('~/Desktop/test_site'), verbose_mode=True)
    new_site.generate()
