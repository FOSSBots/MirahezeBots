from __future__ import unicode_literals, absolute_import, print_function, division

import os
import codecs
from sopel.module import rule, event

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
        bot.say('Hello {}!'.format(trigger.nick))
        bot.known_users_list.append(trigger.nick)
        save_known_users_list(get_filename(bot), bot.known_users_list)
