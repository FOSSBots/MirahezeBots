# Some commands for just goofing around and having fun
# Created by John Bishop for Miraheze

from sopel import module


@module.example('.coffee JohnBishop')
@module.commands('coffee')
def coffee(bot, trigger):
    """
    Makes me give the specified nick a coffee.
    """
    if trigger.group(2) == '':
        bot.reply("To whom should I give this cup of coffee?")
    bot.action("gives %s a nice warm cup of coffee" % (trigger.group(2)), trigger.sender)


@module.example('.hug JohnBishop')
@module.commands('hug')
def coffee(bot, trigger):
    """
    Makes me give the specified nick a hug.
    """
    if trigger.group(2) == '':
        bot.reply("To whom should I give this hug?")
    bot.action("gives %s a great big bear hug" % (trigger.group(2)), trigger.sender)


@module.example('.burger JohnBishop')
@module.commands('burger')
def coffee(bot, trigger):
    """
    Makes me give the specified nick a burger.
    """
    if trigger.group(2) == '':
        bot.reply("To whom should I give this cheeseburger?")
    bot.action("gives %s a freshly cooked cheeseburger" % (trigger.group(2)), trigger.sender)


@module.example('.present JohnBishop')
@module.commands('present')
def coffee(bot, trigger):
    """
    Makes me give the specified nick a present.
    """
    if trigger.group(2) == '':
        bot.reply("To whom should I give this present?")
    bot.action("gives %s a present" % (trigger.group(2)), trigger.sender)
