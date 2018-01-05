"""This module provides admin list and access level information."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel.module import commands


@commands('botadmins', 'admins')
def admin_list(bot, trigger):
    """Provide the list of bot admins."""
    admins = bot.config.core.admins
    if len(admins) == 0:
        bot.reply('There are no bot admins')
        return

    admins = ['You' if admin == trigger.nick else admin for admin in admins]
    admins_str = ', '.join(admins[:-1]) + ' and ' + admins[-1]
    bot.reply('The bot\'s admins are: ' + admins_str)


@commands('accesslevel', 'access')
def access_level(bot, trigger):
    """Tell user what is his access level for this bot."""
    if trigger.nick == bot.config.core.owner:
        level = 'Owner'
    elif trigger.nick in bot.config.core.admins:
        level = 'Admin'
    else:
        level = 'User'

    bot.say('The access level for {} is {}.'.format(trigger.nick, level))
