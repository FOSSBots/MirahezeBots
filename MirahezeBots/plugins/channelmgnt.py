# coding=utf-8
"""
channelmgnt.py - Sopel Channel Management Plugin
Modified from adminchannel.py - Sopel Channel Admin Module
Copyright 2010-2011, Michael Yanovich, Alek Rollyson, and Elsie Powell
Copyright © 2012, Elad Alfassa <elad@fedoraproject.org>
Licensed under the Eiffel Forum License 2.
https://sopel.chat
"""
import re
import time

from sopel import formatting
from sopel.module import (
    commands, example, priority, OP, require_chanmsg, require_admin
)
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.tools import Identifier
from MirahezeBots.utils import jsonparser as jp
from sopel.tools import SopelMemory


class ChannelmgntSection(StaticSection):
    datafile = ValidatedAttribute('datafile', str)
    support_channel = ValidatedAttribute('support_channel', str)


def setup(bot):
    bot.config.define_section('channelmgnt', ChannelmgntSection)
    bot.memory["channelmgnt"] = SopelMemory()
    bot.memory["channelmgnt"]["jdcache"] = jp.createdict(bot.settings.channelmgnt.datafile)


def configure(config):
    config.define_section('channelmgnt', ChannelmgntSection, validate=False)
    config.channelmgnt.configure_setting('datafile', 'Where is the datafile for channelmgnt?')
    config.channelmgnt.configure_setting('support_channel', 'What channel should users ask for help in?')


def default_mask(trigger):
    welcome = formatting.color('Welcome to:', formatting.colors.PURPLE)
    chan = formatting.color(trigger.sender, formatting.colors.TEAL)
    topic_ = formatting.bold('Topic:')
    topic_ = formatting.color('| ' + topic_, formatting.colors.PURPLE)
    arg = formatting.color('{}', formatting.colors.GREEN)
    return '{} {} {} {}'.format(welcome, chan, topic_, arg)


def chanopget(channeldata, chanopsjson):
    chanops = []
    if 'inherits-from' in channeldata.keys():
        for x in channeldata["inherits-from"]:
            y = channelparse(channel=x, cachedjson=chanopsjson)
            chanops = chanops + y[0]["chanops"]
    if 'chanops' in channeldata.keys():
        chanops = chanops + (channeldata["chanops"])
    if chanops == []:
        return False
    else:
        return chanops


def channelparse(channel, cachedjson):
    if channel in cachedjson.keys():
        channeldata = cachedjson[channel]
        return channeldata, cachedjson
    else:
        return False


def get_chanops(channel, cachedjson):
    channeldata = channelparse(channel=channel, cachedjson=cachedjson)
    if not channeldata:
        chanops = False
    else:
        chanops = chanopget(channeldata[0], channeldata[1])
    return chanops


def makemodechange(bot, trigger, mode, isusermode=False, isbqmode=False):
    chanops = get_chanops(str(trigger.sender), bot.memory["channelmgnt"]["jdcache"])
    if chanops:
        if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.account in chanops:
            bot.say('Attempting to OP...')
            bot.say('op ' + trigger.sender, 'ChanServ')
            time.sleep(1)
        if isusermode and not trigger.group(2):
            bot.write(['MODE', trigger.sender, mode, trigger.nick])
        elif isusermode and trigger.account in chanops:
            bot.write(['MODE', trigger.sender, mode, trigger.group(2)])
        elif isbqmode and trigger.account in chanops:
            bot.write(['MODE', trigger.sender, mode, parse_host_mask(trigger.group().split())])
        elif trigger.account in chanops:
            bot.write(['MODE', trigger.sender, mode])
        else:
            bot.reply('Access Denied. If in error, please contact the channel founder.')

    else:
        bot.reply('No ChanOps Found. Please ask for assistance in {}'.format(bot.settings.channelmgnt.support_channel))


@require_chanmsg
@commands('chanmode')
@example('.chanmode +mz')
def chanmode(bot, trigger):
    """
    Command to change channel mode.
    """
    makemodechange(bot, trigger, trigger.group(2), isusermode=False)


@require_chanmsg
@commands('op')
@example('.op Zppix')
def op(bot, trigger):
    """
    Command to op users in a room. If no nick is given, Sopel will op the nick who sent the command.
    """
    makemodechange(bot, trigger, '+o', isusermode=True)


@require_chanmsg
@commands('deop')
@example('.deop Zppix')
def deop(bot, trigger):
    """
    Command to deop users in a room. If no nick is given, Sopel will deop the nick who sent the command.
    """
    makemodechange(bot, trigger, '-o', isusermode=True)


@require_chanmsg
@commands('voice')
@example('.voice Zppix')
def voice(bot, trigger):
    """
    Command to voice users in a room. If no nick is given, Sopel will voice the nick who sent the command.
    """
    makemodechange(bot, trigger, '+v', isusermode=True)


@require_chanmsg
@commands('devoice')
@example('.devoice Zppix')
def devoice(bot, trigger):
    """
    Command to devoice users in a room. If no nick is given, the nick who sent the command will be devoiced.
    """
    makemodechange(bot, trigger, '-v', isusermode=True)


@require_chanmsg
@commands('kick')
@priority('high')
@example('.kick Zppix')
def kick(bot, trigger):
    """Kick a user from the channel."""
    chanops = get_chanops(str(trigger.sender), bot.memory["channelmgnt"]["jdcache"])
    if chanops:
        if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.account in chanops:
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
        if nick != bot.config.core.nick and trigger.account in chanops:
            bot.write(['KICK', channel, nick, ':' + reason])
        else:
            bot.reply('Access Denied. If in error, please contact the channel founder.')
    else:
        bot.reply('No ChanOps Found. Please ask for assistance in {}'.format(bot.settings.channelmgnt.support_channel))


def parse_host_mask(text):
    argc = len(text)
    if argc < 2:
        return
    opt = Identifier(text[1])
    mask = opt
    if not opt.is_nick():
        if argc < 3:
            return
        mask = text[2]
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
@example('.ban Zppix')
def ban(bot, trigger):
    """Ban a user from the channel. The bot must be a channel operator for this command to work.
    """
    makemodechange(bot, trigger, '+b', isbqmode=True)


@require_chanmsg
@commands('unban')
@example('.unban Zppix')
def unban(bot, trigger):
    """Unban a user from the channel. The bot must be a channel operator for this command to work.
    """
    makemodechange(bot, trigger, '-b', isbqmode=True)


@require_chanmsg
@commands('quiet')
@example('.quiet Zppix')
def quiet(bot, trigger):
    """Quiet a user. The bot must be a channel operator for this command to work.
    """
    makemodechange(bot, trigger, '+q', isbqmode=True)


@require_chanmsg
@commands('unquiet')
@example('.unquiet Zppix')
def unquiet(bot, trigger):
    """Unquiet a user. The bot must be a channel operator for this command to work.
    """
    makemodechange(bot, trigger, '-q', isbqmode=True)


@require_chanmsg
@commands('kickban', 'kb')
@example('.kickban [#chan] user1 user!*@* get out of here')
@priority('high')
def kickban(bot, trigger):
    """Kick and ban a user from the channel. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(str(trigger.sender), bot.memory["channelmgnt"]["jdcache"])
    if chanops:
        if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.account in chanops:
            bot.say('Please wait...')
            bot.say('op ' + trigger.sender, 'ChanServ')
            time.sleep(1)
        text = trigger.group().split()
        argc = len(text)
        if argc < 3:
            bot.reply('Syntax is: .kickban <nick> <reason>')
            return
        opt = Identifier(text[1])
        nick = opt
        mask = text[2] if any([s in text[2] for s in "!@*"]) else ''
        channel = trigger.sender
        reasonidx = 3 if mask != '' else 2
        if not opt.is_nick():
            if argc < 5:
                bot.reply('Syntax is: .kickban <nick> <reason>')
                return
            channel = opt
            nick = text[2]
            mask = text[3] if any([s in text[3] for s in "!@*"]) else ''
            reasonidx = 4 if mask != '' else 3
        reason = ' '.join(text[reasonidx:])
        mask = parse_host_mask(trigger.group().split())
        if mask == '':
            mask = nick + '!*@*'
        if trigger.account in chanops:
            bot.write(['MODE', channel, '+b', mask])
            bot.write(['KICK', channel, nick, ':' + reason])
        else:
            bot.reply('Access Denied. If in error, please contact the channel founder.')
    else:
        bot.reply('No ChanOps Found. Please ask for assistance in {}'.format(bot.settings.channelmgnt.support_channel))


@require_chanmsg
@commands('topic')
@example('.topic Your Great New Topic')
def topic(bot, trigger):
    """Change the channel topic. The bot must be a channel operator for this command to work.
    """
    chanops = get_chanops(str(trigger.sender), bot.memory["channelmgnt"]["jdcache"])
    if chanops:
        if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.account in chanops:
            bot.say('Please wait...')
            bot.say('op ' + trigger.sender, 'ChanServ')
            time.sleep(1)
        if not trigger.group(2):
            return
        channel = trigger.sender.lower()

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
        if trigger.account in chanops:
            bot.write(('TOPIC', channel + ' :' + topic))
        else:
            bot.reply('Access Denied. If in error, please contact the channel founder.')
    else:
        bot.reply('No ChanOps Found. Please ask for assistance in {}'.format(bot.settings.channelmgnt.support_channel))


@require_chanmsg
@commands('tmask')
@example('.tmask Welcome to My Channel | Info: {}')
def set_mask(bot, trigger):
    """Set the topic mask to use for the current channel. Within the topic mask, {} is used to allow substituting in chunks of text. This mask is used when running the 'topic' command.
    """
    chanops = get_chanops(str(trigger.sender), bot.memory["channelmgnt"]["jdcache"])
    if chanops:
        if trigger.account in chanops:
            bot.db.set_channel_value(trigger.sender, 'topic_mask', trigger.group(2))
            bot.say("Gotcha, " + trigger.account)
        else:
            bot.reply('Access Denied. If in error, please contact the channel founder.')
    else:
        bot.reply('No ChanOps Found. Please ask for assistance in {}'.format(bot.settings.channelmgnt.support_channel))


@require_chanmsg
@commands('showmask')
@example('showmask')
def show_mask(bot, trigger):
    """Show the topic mask for the current channel."""
    mask = bot.db.get_channel_value(trigger.sender, 'topic_mask')
    mask = mask or default_mask(trigger)
    bot.say(mask)


@require_chanmsg
@commands('invite')
def invite_user(bot, trigger):
    """
    Command to invite users to a room.
    """
    chanops = get_chanops(str(trigger.sender), bot.memory["channelmgnt"]["jdcache"])
    channel = trigger.sender
    if chanops:
        if bot.channels[trigger.sender].privileges[bot.nick] < OP and trigger.account in chanops:
            bot.say('Please wait...')
            bot.say('op ' + trigger.sender, 'ChanServ')
            time.sleep(1)
            nick = trigger.group(2)
            if not nick:
                bot.say(trigger.account + ": No user specified.", trigger.sender)
            elif trigger.account in chanops:
                bot.write(['INVITE', channel, nick])
            else:
                bot.reply('Access Denied. If in error, please contact the channel founder.')
    else:
        bot.reply('No ChanOps Found. Please ask for assistance in {}'.format(bot.settings.channelmgnt.support_channel))


@require_admin(message="Only admins may purge cache.")
@commands('resetchanopcache')
def reset_chanop_cache(bot, trigger):
    """
    Reset the cache of the channel management data file
    """
    bot.reply("Refreshing Cache...")
    bot.memory["channelmgnt"]["jdcache"] = jp.createdict(bot.settings.channelmgnt.datafile)
    bot.reply("Cache refreshed")


@require_admin(message="Only admins may check cache")
@commands('checkchanopcache')
def check_chanop_cache(bot, trigger):
    """
    Validate the cache matches the copy on disk
    """
    result = jp.validatecache(bot.settings.channelmgnt.datafile, bot.memory["channelmgnt"]["jdcache"])
    if result:
        bot.reply("Cache is correct.")
    else:
        bot.reply("Cache does not match on-disk copy")
