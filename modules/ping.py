from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.module import rule, priority, thread, commands

@commands('ping')
def ping2(bot, trigger):
    bot.say('Pong!')
"""
ping.py - Sopel Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://sopel.chat
"""
