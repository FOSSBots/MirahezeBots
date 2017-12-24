from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import commands


@commands('botadmins','admins')
def admin_list(bot, trigger):
    admin_accounts = bot.config.core.admin_accounts
    if len(admin_accounts) == 0:
        bot.reply('There are no bot admins')
        return

    admin_accounts = ['You' if admin == trigger.nick else admin for admin in admin_accounts]
    bot.reply('The bot\'s admins are: ' + ', '.join(admin_accounts[:-1]) + ' and ' + admin_accounts[-1])


@commands('accesslevel')
def access_level(bot, trigger):
    if trigger.nick == bot.config.core.owner:
        level = 'Owner'
    elif trigger.nick in bot.config.core.admin_accounts:
        level = 'Admin'
    else:
        level = 'User'

    bot.say('The access level for {} is {}.'.format(trigger.nick, level))