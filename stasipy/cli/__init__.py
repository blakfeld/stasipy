"""
cli:
    Generic Abstract class for the Stasipy CLI.

Author: Corwin Brown
Date: 05/02/2016
"""

from abc import ABCMeta, abstractmethod

import argparse


class StasipyCLI(object):
    __metaclass__ = ABCMeta

    _description = None

    def __init__(self, args):
        """
        Constructor.

        Args:
            args (list):    Args from the command line. I expect this to
                                basically be: sys.argv[2:]
        """
        self.args = args

        self.parser = self._setup_base_parser()

    def _setup_base_parser(self):
        """
        Construct a base parser object that has options that I expect
            every subcommand to want access to.

        Returns:
            ArgumentParser object.
        """

        parser = argparse.ArgumentParser(self.description)

        parser.add_argument('site_path',
                            type=str,
                            metavar='SITE-PATH',
                            help='The path to the site you wish to reference.')
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            default=False,
                            help='Toggle verbose mode.')
        parser.add_argument('-y',
                            dest='skip_confirm',
                            action='store_true',
                            default=False,
                            help='Answer yes to all confirm dialogs.')
        return parser

    def parse(self):
        """
        Parse out command line args.
        """
        self.parsed_args = self.parser.parse_args(self.args)

    @property
    def description(self):
        """
        Get the description of the commandline tool.
        """
        if self._description is None:
            raise NotImplementedError('Description not implemented.')

        return self._description

    @abstractmethod
    def run(self):
        """
        Execute the command line task.
        """
        raise NotImplementedError()
