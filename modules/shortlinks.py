"""This module expands links to various websites"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
from sopel.module import rule, commands, example


@commands('github', 'gh')
@example('.github user')
def ghuser(bot, trigger):
	""" Will provide a link to the user provided on github """
    try:
        bot.say("https://github.com/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .github user', trigger.sender)


@commands('redditu')
@example('.redditu example')
def redditu(bot, trigger):
	""" Will link to the reddit user provided """
    try:
        bot.say("https://reddit.com/u/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .redditu example', trigger.sender)


@commands('subred')
@example('.subred example')
def redditr(bot, trigger):
	""" Will link to the provided subreddit """
    try:
        bot.say("https://reddit.com/r/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .subred example', trigger.sender)


@commands('wmca')
@example('.wmca example')
def wmca(bot, trigger):
	""" Provides link to the Central Auth for the provided Wikimedia account """
    try:
        bot.say("https://meta.wikimedia.org/wiki/Special:CentralAuth/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .wmca example', trigger.sender)


@commands('mhca')
@example('.mhca example')
def mhca(bot, trigger):
	""" Provides link to the Central Auth for the provided Miraheze account """
    try:
        bot.say("https://meta.miraheze.org/wiki/Special:CentralAuth/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .mhca example', trigger.sender)


@commands('tw')
@example('.tw user')
def twlink(bot, trigger):
	""" Provides a link to the provided Twitter user """
    try:
        bot.say("https://twitter.com/" + trigger.group(2))
    except TypeError:
        bot.say('Syntax: .tw user', trigger.sender)


@commands('mh')
@example('.mh wiki page')
def mhwiki(bot, trigger):
	""" Links to the provided wiki and/or page on Miraheze """
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
