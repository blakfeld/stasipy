"""
init.py:
    Class for the 'init' subcommand.

Author: Corwin Brown
Date: 05/01/2016
"""
from __future__ import absolute_import

from stasipy.stasipy import Stasipy
from stasipy.cli import StasipyCLI


class StasipyInit(StasipyCLI):
    """
    CLI command to initialize a new Stasipy site.
    """

    _description = 'Initialize a new Stasipy site.'

    def __init__(self, args):
        """
        Constructor

        Args:
            args (str):     Command line args to parse (Think "sys.argv[1:]")
        """
        super(self.__class__, self).__init__(args=args)

    def parse(self):
        """
        Parse CLI args.
        """
        self.parser.add_argument('-n', '--site-name',
                                 type=str,
                                 metavar='SITE-NAME',
                                 help='The name of the site to generate.')

        super(self.__class__, self).parse()

    def run(self):
        """
        Execute.
        """
        stasipy = Stasipy(
            base_site_path=self.parsed_args.site_path,
            site_name=self.parsed_args.site_name,
            verbose_mode=self.parsed_args.verbose,
            skip_confirm=self.parsed_args.skip_confirm,
        )
        stasipy.init()

    @property
    def description(self):
        return self._description
