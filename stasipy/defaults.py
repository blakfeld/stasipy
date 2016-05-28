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
        'nav_items': [
            {
                'title': 'Test Page 1',
                'href': '/sample_page/test_page1'
            }
        ],
        'time_format': '%m/%d/%Y'
    }
