# Some commands for just goofing around and having fun
# Created by John Bishop for Miraheze

from sopel import module

@module.commands('coffee')
def coffee(bot, trigger):
    if trigger.group(2) == '':
      bot.reply("To whom should I give this cup of coffee?")
    bot.action("gives %s a nice warm cup of coffee" % (trigger.group(2)), trigger.sender)
