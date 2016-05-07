"""
defaults.py:
    Default values for various settings.

Author: Corwin Brown
Date: 05/07/2016
"""
from __future__ import absolute_import


class StasipyDefaults:
    default_site_config = {
        'maintainer': '<put your name here>',
        'email': '<put your email here>',
    }

    default_site_structure = [
        {
            'src': [
                {'templates': []},
                {'static': []},
                {'pages': []},
                {'posts': []},
            ],
        },
        {
            'out': [
                {'pages': []},
                {'posts': []},
                'index.html',
            ]
        },
        'siteconfig.yml',
    ]
