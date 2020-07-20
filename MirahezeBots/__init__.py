# coding=utf8
"""MirahezeBot Plugins
Custom Sopel Plugins For Miraheze Bots
"""
from __future__ import unicode_literals, absolute_import, division, print_function

try:
    from .MirahezeBots import *
except ImportError:
    # probably being imported by setup.py to get metadata before installation
    # no cause for alarm
    pass

__author__ = 'MirahezeBot Contributors'
__email__ = 'bots@miraheze.org'
__version__ = '8'
