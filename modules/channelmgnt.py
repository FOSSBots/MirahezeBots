# coding=utf-8
"""
Modified from the original
adminchannel.py - Sopel Channel Admin Module
Copyright 2010-2011, Michael Yanovich, Alek Rollyson, and Elsie Powell
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.

https://sopel.chat
"""
from __future__ import unicode_literals, absolute_import, print_function, division

import re
import time

from sopel import formatting
from sopel.module import (
    commands, example, priority, OP, require_chanmsg
)
from sopel.tools import Identifier


def default_mask(trigger):
    welcome = formatting.color('Welcome to:', formatting.colors.PURPLE)
    chan = formatting.color(trigger.sender, formatting.colors.TEAL)
    topic_ = formatting.bold('Topic:')
    topic_ = formatting.color('| ' + topic_, formatting.colors.PURPLE)
    arg = formatting.color('{}', formatting.colors.GREEN)
    return '{} {} {} {}'.format(welcome, chan, topic_, arg)


def get_chanops(bot, trigger):
    chanops = ''
    if str(trigger.sender) == '##RhinosF1':
        chanops = ['RhinosF1', 'Zppix', 'Reception123', 'LakesideMiners', 'Vermont', 'Oshwah', 'TheSandDoctor', 'dtm', 'Kb03', 'Aldnonymous', 'ShakespeareFan00', 'Qui', 'Southparkfan', 'gonzobot']
    elif str(trigger.sender) == '##acme':
        chanops = ['RhinosF1', 'tex', 'B|ack0p']
    elif str(trigger.sender) == '#miraheze' or str(trigger.sender) == '#miraheze-offtopic':
        chanops = ['Southparkfan', 'NDKilla', 'labster', 'Reception123', 'Voidwalker', 'Void|bot', 'JohnLewis', 'Paladox', 'RhinosF1']
    elif str(trigger.sender) == '#miraheze-cvt' or str(trigger.sender) == '#miraheze-cvt-private':
        chanops = ['NDKilla', 'Voidwalker', 'Reception123', 'Zppix', 'The_Pionner', 'JohnLewis']
    elif str(trigger.sender) == '#miraheze-testwiki':
        chanops = ['Reception123', 'NDKilla', 'Voidwalker']
    elif str(trigger.sender) == '#miraheze-testwiki-es':
        chanops = ['AlvaroMolina', 'Reception123', 'NDKilla', 'Voidwalker']
    elif str(trigger.sender) == '#ZppixBot':
        chanops = ['Zppix', 'Reception123', 'Voidwalker']
    elif str(trigger.sender) == '#testadminwiki':
        chanops = ['MacFan4000', 'Voidwalker', 'AlvaroMolina']
    elif str(trigger.sender) == '##CyberBogan':
        chanops = ['NeoBogan', 'Oshwah', 'enterprisey', 'Havyk', 'Athyria', 'LakesideMiners', 'foks', 'Jobe', 'MarxLenin99', 'SQLDb', 'TxHadriel', 'ShakespeareFan00', 'Zppix', 'KSFT']
    elif str(trigger.sender) == '##Zppix-Wikipedia':
        chanops = ['Zppix', 'tom29739', 'SwisterTwister', 'Snowycats', 'DatGuy', 'mattwj2002']
    else:
        bot.say('Please ask in #ZppixBot for assistance configuring the channel management module.', trigger.sender)
    return chanops


@require_chanmsg
@commands('op')
def op(bot, trigger):
    """
    Command to op users in a room. If no nick is given, Sopel will op the nick who sent the command
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "+o", nick])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('deop')
def deop(bot, trigger):
    """
    Command to deop users in a room. If no nick is given, Sopel will deop the nick who sent the command
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "-o", nick])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('voice')
def voice(bot, trigger):
    """
    Command to voice users in a room. If no nick is given, Sopel will voice the nick who sent the command
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "+v", nick])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('devoice')
def devoice(bot, trigger):
    """
    Command to devoice users in a room. If no nick is given, the nick who sent the command will be devoiced
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    nick = trigger.group(2)
    channel = trigger.sender
    if not nick:
        nick = trigger.nick
    if trigger.nick in chanops:
        bot.write(['MODE', channel, "-v", nick])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('kick')
@priority('high')
def kick(bot, trigger):
    """Kick a user from the channel."""
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    nick = opt
    channel = trigger.sender
    reasonidx = 2
    if not opt.is_nick():
        if argc < 3:
            return
        nick = text[2]
        channel = opt
        reasonidx = 3
    reason = ' '.join(text[reasonidx:])
    if nick != bot.config.core.nick and trigger.sender in chanops:
        bot.write(['KICK', channel, nick, ':' + reason])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


def configureHostMask(mask):
    if mask == '*!*@*':
        return mask
    if re.match('^[^.@!/]+$', mask) is not None:
        return '%s!*@*' % mask
    if re.match('^[^@!]+$', mask) is not None:
        return '*!*@%s' % mask

    m = re.match('^([^!@]+)@$', mask)
    if m is not None:
        return '*!%s@*' % m.group(1)

    m = re.match('^([^!@]+)@([^@!]+)$', mask)
    if m is not None:
        return '*!%s@%s' % (m.group(1), m.group(2))

    m = re.match('^([^!@]+)!(^[!@]+)@?$', mask)
    if m is not None:
        return '%s!%s@*' % (m.group(1), m.group(2))
    return ''


@require_chanmsg
@commands('ban')
@priority('high')
def ban(bot, trigger):
    chanops = get_chanops(bot, trigger)
    """Ban a user from the channel. The bot must be a channel operator for this command to work.
    """
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    banmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '+b', banmask])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('unban')
def unban(bot, trigger):
    """Unban a user from the channel. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    banmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        channel = opt
        banmask = text[2]
    banmask = configureHostMask(banmask)
    if banmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '-b', banmask])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('quiet')
def quiet(bot, trigger):
    """Quiet a user. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    quietmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        quietmask = text[2]
        channel = opt
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '+q', quietmask])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('unquiet')
def unquiet(bot, trigger):
    """Unquiet a user. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    quietmask = opt
    channel = trigger.sender
    if not opt.is_nick():
        if argc < 3:
            return
        quietmask = text[2]
        channel = opt
    quietmask = configureHostMask(quietmask)
    if quietmask == '':
        return
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '-q', quietmask])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('kickban', 'kb')
@example('.kickban [#chan] user1 user!*@* get out of here')
@priority('high')
def kickban(bot, trigger):
    """Kick and ban a user from the channel. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    text = trigger.group().split()
    argc = len(text)
    if argc < 3:
        return
    opt = Identifier(text[1])
    nick = opt
    mask = text[2] if any([s in text[2] for s in "!@*"]) else ''
    channel = trigger.sender
    reasonidx = 3 if mask != '' else 2
    if not opt.is_nick():
        if argc < 5:
            return
        channel = opt
        nick = text[2]
        mask = text[3] if any([s in text[3] for s in "!@*"]) else ''
        reasonidx = 4 if mask != '' else 3
    reason = ' '.join(text[reasonidx:])
    mask = configureHostMask(mask)
    if mask == '':
        mask = nick + '!*@*'
    if trigger.nick in chanops:
        bot.write(['MODE', channel, '+b', mask])
        bot.write(['KICK', channel, nick, ':' + reason])
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('topic')
def topic(bot, trigger):
    """Change the channel topic. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(bot, trigger)
    if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.nick in chanops:
        bot.say('Please wait...')
        bot.say('op ' + trigger.sender, 'ChanServ')
        time.sleep(1)
    if not trigger.group(2):
        return
    channel = trigger.sender.lower()

    narg = 1
    mask = None
    mask = bot.db.get_channel_value(channel, 'topic_mask')
    mask = mask or default_mask(trigger)
    mask = mask.replace('%s', '{}')
    narg = len(re.findall('{}', mask))

    top = trigger.group(2)
    args = []
    if top:
        args = top.split('~', narg)

    if len(args) != narg:
        message = "Not enough arguments. You gave {}, it requires {}.".format(
            len(args), narg)
        return bot.say(message)
    topic = mask.format(*args)
    if trigger.nick in chanops:
        bot.write(('TOPIC', channel + ' :' + topic))
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('tmask')
def set_mask(bot, trigger):
    """Set the topic mask to use for the current channel. Within the topic mask, {} is used to allow substituting in chunks of text. This mask is used when running the 'topic' command.
    """
    chanops = get_chanops(bot, trigger)
    if trigger.sender in chanops:
        bot.db.set_channel_value(trigger.sender, 'topic_mask', trigger.group(2))
        bot.say("Gotcha, " + trigger.nick)
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')


@require_chanmsg
@commands('showmask')
def show_mask(bot, trigger):
    """Show the topic mask for the current channel."""
    chanops = get_chanops(bot, trigger)
    if trigger.nick in chanops:
        mask = bot.db.get_channel_value(trigger.sender, 'topic_mask')
        mask = mask or default_mask(trigger)
        bot.say(mask)
    else:
        bot.reply('Access Denied. If in error, please contact the channel founder.')
