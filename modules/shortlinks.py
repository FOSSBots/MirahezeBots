"""This module expands links to various websites"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
from sopel.module import rule, commands, example


@commands('github', 'gh')
@example('.github user')
"""Expands a link to github."""
def ghuser(bot, trigger):
    try:
        bot.say("https://github.com/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .github user', trigger.sender)


@commands('redditu')
@example('.redditu example')
"""Expands a link to reddit/u."""
def redditu(bot, trigger):
    try:
        bot.say("https://reddit.com/u/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .redditu example', trigger.sender)


@commands('subred')
@example('.subred example')
"""Expands a link to reddit/r."""
def redditr(bot, trigger):
    try:
        bot.say("https://reddit.com/r/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .subred example', trigger.sender)


@commands('wmca')
@example('.wmca example')
"""Expands a link to Wikimedia CentralAuth."""
def wmca(bot, trigger):
    try:
        bot.say("https://meta.wikimedia.org/wiki/Special:CentralAuth/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .wmca example', trigger.sender)


@commands('mhca')
@example('.mhca example')
"""Expands a link to Miraheze Central Auth."""
def mhca(bot, trigger):
    try:
        bot.say("https://meta.miraheze.org/wiki/Special:CentralAuth/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .mhca example', trigger.sender)


@commands('tw')
@example('.tw user')
"""Expands a link to Twitter."""
def twlink(bot, trigger):
    try:
        bot.say("https://twitter.com/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .tw user', trigger.sender)


@commands('mh')
@example('.mh wiki page')
"""Expands a link to Miraheze wikis."""
def mhwiki(bot, trigger):
    try:
        options = trigger.group(2).split(" ")
        if len(options) == 1:
            page = options[0]
            bot.say("https://meta.miraheze.org/wiki/" + page)
        elif len(options) == 2:
            wiki = options[0]
            page = options[1]
            bot.say("https://" + wiki + ".miraheze.org/wiki/" + page)
    except AttributeError:
        bot.say('Syntax: .mh wiki page', trigger.sender)
