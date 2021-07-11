"""welcome.py - Plugin to welcome users upon joining the channel."""

import codecs
import os
import re
from typing import Union, List, Dict

from sopel import bot, trigger
from sopel.tools import Identifier
from sopel.plugin import commands, event, example, rule

DEFAULT_CHANNEL = '#miraheze'
USERNAME_RE = re.compile(r'[A-Za-z0-9\[\]\{\}\-_|`]+$')
CHANNEL_RE = re.compile(r'#[A-Za-z0-9#\-]+$')


def send_welcome(nick: Identifier, chan: Identifier) -> Union[None, str]:
    """Find the message to be sent."""
    if chan == '#miraheze' and nick[:4] != 'Not-':
        return f'Hello {nick}! If you have any questions, feel free to ask and someone should answer soon.'
    if chan == '#miraheze-cvt':
        return f'Welcome {nick}. If you need to report spam or abuse, please feel free to notify any of the voiced (+v) users, if it contains personal information you can pm them, or email us at cvt [at] miraheze.org'  # noqa: E501
    return None


def setup(instance: bot) -> None:
    """Do required setup for this module."""
    instance.known_users_filename = os.path.join(instance.config.core.homedir, f'{instance.nick}-{instance.config.core.host}.known_users.db')
    instance.known_users_list = load_known_users_list(instance.known_users_filename)


def load_known_users_list(filename: str) -> Dict[str, List[str]]:
    """Load list of known users from database file."""
    known_users = {}  # type: Dict[str, List[str]]
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


def save_known_users_list(filename: str, known_users_list: Dict) -> None:
    """Save list of known users to database file."""
    f = codecs.open(filename, 'w', encoding='utf-8')
    for channel in known_users_list:
        for user in known_users_list[channel]:
            f.write(f'{channel}\t{user}\n')
    f.close()


@event('JOIN')
@rule('.*')
def welcome_user(instance: bot, message: trigger) -> None:
    """Welcome users upon joining the channel."""
    if message.nick == instance.nick:
        return

    if message.sender not in instance.known_users_list:
        instance.known_users_list[message.sender] = []
    if message.account == '*' and message.nick not in instance.known_users_list[message.sender]:
        instance.known_users_list[message.sender].append(message.nick)
        welcome = send_welcome(message.nick, message.sender)
        if welcome is not None:
            instance.say(welcome)
    else:
        if (message.account and message.nick) not in instance.known_users_list[message.sender]:
            instance.known_users_list[message.sender].append(message.account)
            welcome = send_welcome(message.nick, message.sender)
            if welcome is not None:
                instance.say(welcome)

    save_known_users_list(instance.known_users_filename, instance.known_users_list)


@commands('add_known', 'adduser')
@example('.add_known nick #example or .adduser nick #example')
def add_known_user(instance: bot, message: trigger) -> None:
    """Add user to known users list."""
    if message.account not in instance.config.core.admin_accounts:
        instance.reply('Only bot admins can add people to the known users list.')
        return

    username = message.group(3)
    if message.group(4):
        channel = message.group(4)
    elif message.sender[0] == '#':
        channel = message.sender
    else:
        channel = DEFAULT_CHANNEL

    if not USERNAME_RE.match(username):
        instance.reply(f'Invalid username: {username}')
        return

    if not CHANNEL_RE.match(channel):
        instance.reply(f'Invalid channel name: {channel}')
        return

    if channel not in instance.known_users_list:
        instance.known_users_list[channel] = []

    if username in instance.known_users_list[channel]:
        instance.say(f'{username} is already added to known users list of channel {channel}')
        return

    instance.known_users_list[channel].append(username)
    save_known_users_list(instance.known_users_filename, instance.known_users_list)
    instance.say(f'Okay, {username} is now added to known users list of channel {channel}')
