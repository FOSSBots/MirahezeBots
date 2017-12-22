from __future__ import unicode_literals, absolute_import, print_function, division

import os
import re
import codecs
from sopel.module import rule, event, commands, example

ADMIN_LIST = ['Reception123', 'MacFan400', 'Zppix', 'SwisterTwister', 'paladox']
DEFAULT_CHANNEL = '#miraheze'
USERNAME_RE = re.compile('[A-Za-z0-9\[\]\{\}\-_|`]+$')
CHANNEL_RE = re.compile('#[A-Za-z0-9]+$')

def get_filename(bot):
    name = '{}-{}.known_users.db'.format(bot.nick, bot.config.core.host)
    return os.path.join(bot.config.core.homedir, name)


def setup(bot):
    bot.known_users_filename = get_filename(bot)
    bot.known_users_list = load_known_users_list(bot.known_users_filename)


def load_known_users_list(filename):
    known_users = {}
    if os.path.isfile(filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        for line in f:
            line = line.rstrip('\n')
            if '\t' in line:
                channel, username = line.split('\t')
            else:
                channel = DEFAULT_CHANNEL
                username = line

            if channel in known_users:
                known_users[channel].append(username)
            else:
                known_users[channel] = [username]
    return known_users


def save_known_users_list(filename, known_users_list):
    f = codecs.open(filename, 'w', encoding='utf-8')
    for channel in known_users_list:
        for user in known_users_list[channel]:
            f.write('{}\t{}\n'.format(channel, user))
    f.close()


@event('JOIN')
@rule('.*')
def welcome_user(bot, trigger):
    """Welcome users upon joining the channel"""
    if trigger.nick == bot.nick:
        return

    if trigger.sender not in bot.known_users_list:
        bot.known_users_list[trigger.sender] = []

    if trigger.nick not in bot.known_users_list[trigger.sender]:
        if trigger.sender == '#miraheze':
            message = 'Hello {}! If you have any questions feel free to ask and someone should answer soon.'.format(trigger.nick)
        else:
            message = 'Hello {}!'.format(trigger.nick)

        bot.say(message)
        bot.known_users_list[trigger.sender].append(trigger.nick)
        save_known_users_list(get_filename(bot), bot.known_users_list)


@commands('add_known', 'adduser')
@example('.add_known Zppix #miraheze or .adduser Zppix #miraheze')
def add_known_user(bot, trigger):
    if trigger.nick not in ADMIN_LIST:
        bot.reply('Only bot admins can add people to the known users list.')
        return

    username = trigger.group(3)
    if trigger.group(4):
        channel = trigger.group(4)
    elif trigger.sender[0] == '#':
        channel = trigger.sender
    else:
        channel = DEFAULT_CHANNEL

    if not USERNAME_RE.match(username):
        bot.reply('Invalid username: {}'.format(username))
        return

    if not CHANNEL_RE.match(channel):
        bot.reply('Invalid channel name: {}'.format(channel))
        return

    if channel not in bot.known_users_list:
        bot.known_users_list[channel] = []

    if username in bot.known_users_list[channel]:
        bot.say('{} is already added to known users list of channel {}'.format(username, channel))
        return

    bot.known_users_list[channel].append(username)
    save_known_users_list(get_filename(bot), bot.known_users_list)
    bot.say('Okay, {} is now added to known users list of channel {}'.format(username, channel))
