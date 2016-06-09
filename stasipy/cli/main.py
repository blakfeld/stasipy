"""
main.py:
    Main entry point for the CLI.

Author: Corwin Brown
Date: 05/01/2016
"""
from __future__ import absolute_import

import sys

from stasipy.errors import StasipyException

# List of all the valid commands.
VALID_SUBCOMMANDS = [
    'init',
    'generate',
]


def valid_subcommand(subcommand, valid_subcommands):
    """
    Ensure we've specifed a valid subcommand.
    """
    if subcommand in valid_subcommands:
        return True
    else:
        return False


def list_valid_subcommands(valid_subcommands):
    """
    Create a human friendly list of the valid sub commands.

    Args:
        valid_subcommands (list):   A list of the valid commands.
    """

    # Return a string that outputs like:
    #
    #   * command1
    #   * command2
    #   * etc

    output = 'VALID SUBCOMMANDS:\n  * {0}'.format('\n  * '.join(valid_subcommands))

    return output


def main():
    """
    Parse out the the subcommand, then run that module.

    Returns:
        int:     The exit code of the CLI.
    """
    if len(sys.argv) <= 1:
        print("You must enter a subcommand!\n\n{0}\n"
              .format(list_valid_subcommands(VALID_SUBCOMMANDS)))
        return 1

    subcommand = sys.argv[1]
    args = sys.argv[2:]

    if not valid_subcommand(subcommand, VALID_SUBCOMMANDS):
        print("Invalid subcommand!\n\n{0}\n"
              .format(list_valid_subcommands(VALID_SUBCOMMANDS)))
        return 1

    if subcommand == 'init':
        from stasipy.cli.init import StasipyInit as myCLI
    elif subcommand == 'generate':
        from stasipy.cli.generate import StasipyGenerate as myCLI

    cli = myCLI(args)
    try:
        cli.parse()
    except StasipyException as e:
        # TODO: Catch the actual exception, not just everything.
        print('Exception: {0}'.format(e))
        return 1

    try:
        cli.run()
    except StasipyException as e:
        # TODO: Catch the actual exception, not just everything.
        print('Exception: {0}'.format(e))
        return 1
