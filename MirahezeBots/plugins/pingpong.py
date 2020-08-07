"""
ping.py - Sopel Ping Plugin.

Author: Sean B. Palmer, inamidst.com
About: http://sopel.chat
"""

from sopel.module import commands


@commands('ping')
def ping2(bot, trigger):
    """Reply to ping command."""
    bot.say('Pong!')
