"""
stasipy.py:
    Class that contains most of the Stasipy business logic.

Author: Corwin Brown
Date: 05/07/2016
"""
from __future__ import absolute_import

import os
import yaml

import stasipy.utils as utils
from stasipy.defaults import StasipyDefaults


class Stasipy(object):
    """
    Main Stasipy Class.
    """

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

        self._verbose('Creating base site path at: "{0}"'.format(self.base_site_path))
        utils.ensure_directory_exists(self.base_site_path)

        self._verbose('Generating base site.')
        self._create_directory_tree(self.site_structure, self.base_site_path)

        self._verbose('Generating initial "siteconfig.yml" file.')
        self._generate_base_site_config(site_name=self.site_name)

    def _create_directory_tree(self, structure, path):
        """
        Recursively traverse my site_structure data structure and
            create that file tree.

        Args:
            structure (dict|list|str):      The file structure to traverse.
            path (str):                     The path on disk to create the
                                                structure.
        """
        if not structure:
            return

        for node in structure:
            if isinstance(node, dict):
                for sub_node, dirs in node.items():
                    node_path = os.path.join(path, sub_node)
                    self._verbose('Creating directory at: "{0}"'.format(node_path))
                    utils.ensure_directory_exists(node_path)
                    self._create_directory_tree(dirs, node_path)
            elif isinstance(node, list):
                self._create_directory_tree(node, path)
            elif isinstance(node, str):
                node_path = os.path.join(path, node)
                self._verbose('Touching file at: "{0}"'.format(node_path))
                utils.touch(node_path)

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
        pass

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
    new_site.init()
