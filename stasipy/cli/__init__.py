"""
cli:
    Generic Abstract class for the Stasipy CLI.

Author: Corwin Brown
Date: 05/02/2016
"""

from abc import ABCMeta, abstractmethod, abstractproperty

import argparse


class StasipyCLI(object):
    __metaclass__ = ABCMeta

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
                            help='Toggle verbose mode.')
        return parser

    @abstractproperty
    def description():
        """
        Get the description of the commandline tool.
        """
        raise NotImplementedError()

    @abstractmethod
    def parse(self):
        """
        Parse out command line args.
        """
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        """
        Execute the command line task.
        """
        raise NotImplementedError()
