"""
generate.py:
    Class for the 'generate' subcommand.

Author: Corwin Brown
Date: 05/01/2016
"""
from __future__ import absolute_import

from stasipy.stasipy import Stasipy
from stasipy.cli import StasipyCLI


class StasipyGenerate(StasipyCLI):
    """
    CLI command to generate a site.
    """

    _description = 'Generate a site.'

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
        self.parsed_args = self.parser.parse_args(self.args)

    def run(self):
        """
        Execute.
        """
        stasipy = Stasipy(
            base_site_path=self.parsed_args.site_path,
            verbose_mode=self.parsed_args.verbose,
        )
        stasipy.generate()
