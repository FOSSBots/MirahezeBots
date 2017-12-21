from __future__ import unicode_literals, absolute_import, print_function, division

import os
import codecs
from sopel.module import rule, event, commands, example

ADMIN_LIST = ['Reception123', 'Zppix', 'SwisterTwister', 'paladox']

def get_filename(bot):
    name = '{}-{}.known_users.db'.format(bot.nick, bot.config.core.host)
    return os.path.join(bot.config.core.homedir, name)


def setup(bot):
    bot.known_users_filename = get_filename(bot)
    bot.known_users_list = load_known_users_list(bot.known_users_filename)


def load_known_users_list(filename):
    known_users = []
    if os.path.isfile(filename):
        f = codecs.open(filename, 'r', encoding='utf-8')
        for line in f:
            known_users.append(line.rstrip('\n'))
    return known_users


def save_known_users_list(filename, known_users_list):
    f = codecs.open(filename, 'w', encoding='utf-8')
    for user in known_users_list:
        f.write('{}\n'.format(user))
    f.close()


@event('JOIN')
@rule('.*')
def welcome_user(bot, trigger):
    """Welcome users upon joining the channel"""
    if trigger.nick == bot.nick:
        return

    if trigger.nick not in bot.known_users_list:
        if trigger.sender == '#miraheze':
            message = 'Hello {}! If you have any questions feel free to ask and someone should answer soon.'.format(trigger.nick)
        else:
            message = 'Hello {}!'.format(trigger.nick)

        bot.say(message)
        bot.known_users_list.append(trigger.nick)
        save_known_users_list(get_filename(bot), bot.known_users_list)


@commands('add_known', 'adduser')
@example('.add_known Zppix or .adduser Zppix')
def add_known_user(bot, trigger):
    if trigger.nick not in ADMIN_LIST:
        bot.reply('Only bot admins can add people to the known users list.')
        return

    username = trigger.group(2)

    if username in bot.known_users_list:
        bot.say('{} is already added to known users list'.format(username))
        return

    bot.known_users_list.append(username)
    save_known_users_list(get_filename(bot), bot.known_users_list)
    bot.say('Okay, {} is now added to known users list'.format(username))
