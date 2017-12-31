"""
ping.py - Sopel Ping Module.

Author: Sean B. Palmer, inamidst.com
About: http://sopel.chat
"""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel.module import commands


@commands('ping')
def ping2(bot, trigger):
    """Reply to ping command."""
    bot.say('Pong!')
