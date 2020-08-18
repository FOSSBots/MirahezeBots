"""This plugin provides admin list and access level information."""

from sopel.module import commands


@commands('botadmins', 'admins')
def admin_list(bot, trigger):
    """Provide the list of bot admins."""
    admins = bot.config.core.admin_accounts
    if len(admins) == 0:
        bot.reply('There are no bot admins')
        return

    admins = ['You' if admin == trigger.account else admin for admin in admins]
    admins_str = ', '.join(admins[:-1]) + ' and ' + admins[-1]
    bot.reply('The bot\'s admins are: ' + admins_str)


@commands('accesslevel', 'access')
def access_level(bot, trigger):
    """Tell user what access level they have for the bot."""
    if trigger.account == bot.config.core.owner_account:
        level = 'Owner'
    elif trigger.account in bot.config.core.admin_accounts:
        level = 'Admin'
    else:
        level = 'User'

    bot.say('The access level for {} is {}.'.format(trigger.nick, level))
