"""
errors.py:
    Exceptions for Stasipy.

Author: Corwin Brown
Date: 05/07/2016
"""
from __future__ import absolute_import


class StasipyException(Exception):
    """
    Base Exception class for Stasipy.
    """

    def __init__(self, message):
        """
        Constructor
        Args:
            message (str): Error message to display.
        """

        self.message = '{}'.format(message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
