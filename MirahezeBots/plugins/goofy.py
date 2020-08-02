""" Some commands for just goofing around and having fun """

from sopel import module


@module.example('.coffee MirahezeBot')
@module.commands('coffee')
def coffee(bot, trigger):
    """
    Makes me give the specified nick a coffee.
    """
    if trigger.group(2) is None:
        bot.reply("To whom should I give this cup of coffee?")
    else:
        bot.action("gives %s a nice warm cup of coffee." % (trigger.group(2)), trigger.sender)


@module.example('.hug MirahezeBot')
@module.commands('hug')
def hug(bot, trigger):
    """
    Makes me give the specified nick a hug.
    """
    if trigger.group(2) is None:
        bot.reply("To whom should I give this hug?")
    else:
        bot.action("gives %s a great big bear hug." % (trigger.group(2)), trigger.sender)


@module.example('.burger MirahezeBot')
@module.commands('burger')
def burger(bot, trigger):
    """
    Makes me give the specified nick a burger.
    """
    if trigger.group(2) is None:
        bot.reply("To whom should I give this cheeseburger?")
    else:
        bot.action("gives %s a freshly cooked cheeseburger." % (trigger.group(2)), trigger.sender)


@module.example('.present MirahezeBot')
@module.commands('present')
def present(bot, trigger):
    """
    Makes me give the specified nick a present.
    """
    if trigger.group(2) is None:
        bot.reply("To whom should I give this present?")
    else:
        bot.action("gives %s a present." % (trigger.group(2)), trigger.sender)


@module.example('.hotchoc MirahezeBot')
@module.commands('hotchoc', 'hotchocolate')
def hotchoc(bot, trigger):
    """
    Makes me give the specified nick a hot chocolate.
    """
    if trigger.group(2) is None:
        bot.reply("To whom should I give this hot chocolate?")
    else:
        bot.action("gives %s a warm, velvety salted caramel hot chocolate with cream and marhsmellows." % (trigger.group(2)), trigger.sender)
