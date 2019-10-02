"""This module expands links to various websites"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
from sopel.module import rule, commands, example


@commands('github')
@example('.github repo')
def ghrepo(bot, trigger):
    bot.say("https://github.com/" + trigger.group(2))

@commands('redditu')
@example('.redditu example')
def redditu(bot, trigger):
    bot.say("https://reddit.com/u/" + trigger.group(2))
    
@commands('subred')
@example('.subred example')
def redditr(bot, trigger):
    bot.say("https://reddit.com/r/" + trigger.group(2))

