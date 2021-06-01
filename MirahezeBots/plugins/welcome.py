"""welcome.py - Plugin to welcome users upon joining the channel."""

import codecs
import os
import re

from sopel.plugin import commands, event, example, rule

DEFAULT_CHANNEL = '#miraheze'
USERNAME_RE = re.compile(r'[A-Za-z0-9\[\]\{\}\-_|`]+$')
CHANNEL_RE = re.compile(r'#[A-Za-z0-9#\-]+$')


def send_welcome(nick, chan):
    """Find the message to be sent."""
    if chan == '#miraheze' and nick[:4] != 'Not-':
        return f'Hello {nick}! If you have any questions, feel free to ask and someone should answer soon.'
    if chan == '#miraheze-cvt':
        return f'Welcome {nick}. If you need to report spam or abuse, please feel free to notify any of the voiced (+v) users, if it contains personal information you can pm them, or email us at cvt [at] miraheze.org'  # noqa: E501
    return None


def setup(bot):
    """Do required setup for this module."""
    bot.known_users_filename = os.path.join(bot.config.core.homedir, f'{bot.nick}-{bot.config.core.host}.known_users.db')
    bot.known_users_list = load_known_users_list(bot.known_users_filename)


def load_known_users_list(filename):
    """Load list of known users from database file."""
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
    """Save list of known users to database file."""
    f = codecs.open(filename, 'w', encoding='utf-8')
    for channel in known_users_list:
        for user in known_users_list[channel]:
            f.write(f'{channel}\t{user}\n')
    f.close()


@event('JOIN')
@rule('.*')
def welcome_user(bot, trigger):
    """Welcome users upon joining the channel."""
    if trigger.nick == bot.nick:
        return

    if trigger.sender not in bot.known_users_list:
        bot.known_users_list[trigger.sender] = []
    if trigger.account == '*' and trigger.nick not in bot.known_users_list[trigger.sender]:
        bot.known_users_list[trigger.sender].append(trigger.nick)
        welcome = send_welcome(trigger.nick, trigger.sender)
        if welcome is not None:
            bot.say(welcome)
    else:
        if (trigger.account and trigger.nick) not in bot.known_users_list[trigger.sender]:
            bot.known_users_list[trigger.sender].append(trigger.account)
            welcome = send_welcome(trigger.nick, trigger.sender)
            if welcome is not None:
                bot.say(welcome)

    save_known_users_list(bot.known_users_filename, bot.known_users_list)


@commands('add_known', 'adduser')
@example('.add_known nick #example or .adduser nick #example')
def add_known_user(bot, trigger):
    """Add user to known users list."""
    if trigger.account not in bot.config.core.admin_accounts:
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
        bot.reply(f'Invalid username: {username}')
        return

    if not CHANNEL_RE.match(channel):
        bot.reply(f'Invalid channel name: {channel}')
        return

    if channel not in bot.known_users_list:
        bot.known_users_list[channel] = []

    if username in bot.known_users_list[channel]:
        bot.say(f'{username} is already added to known users list of channel {channel}')
        return

    bot.known_users_list[channel].append(username)
    save_known_users_list(bot.known_users_filename, bot.known_users_list)
    bot.say(f'Okay, {username} is now added to known users list of channel {channel}')
