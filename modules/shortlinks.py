"""This module expands links to various websites"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
from sopel.module import rule, commands, example


@commands('github')
@example('.github repo')
def ghrepo(bot, trigger):
    bot.say(("https://github.com/{}").format(trigger.group(2)), trigger.sender())
