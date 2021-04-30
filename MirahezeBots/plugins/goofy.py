"""Some commands for just goofing around and having fun."""

from sopel.module import commands, example


@example('.coffee MirahezeBot')
@commands('coffee')
def coffee(bot, trigger):
    """Make me give the specified nick a coffee."""
    if trigger.group(2) is None:
        bot.reply('To whom should I give this cup of coffee?')
    else:
        bot.action(f'gives {trigger.group(2)} a nice warm cup of coffee.', trigger.sender)


@example('.hug MirahezeBot')
@commands('hug')
def hug(bot, trigger):
    """Make me give the specified nick a hug."""
    if trigger.group(2) is None:
        bot.reply('To whom should I give this hug?')
    else:
        bot.action(f'gives {trigger.group(2)} a great big bear hug.', trigger.sender)


@example('.burger MirahezeBot')
@commands('burger')
def burger(bot, trigger):
    """Make me give the specified nick a burger."""
    if trigger.group(2) is None:
        bot.reply('To whom should I give this cheeseburger?')
    else:
        bot.action(f'gives {trigger.group(2)} a freshly cooked cheeseburger.', trigger.sender)


@example('.present MirahezeBot')
@commands('present')
def present(bot, trigger):
    """Make me give the specified nick a present."""
    if trigger.group(2) is None:
        bot.reply('To whom should I give this present?')
    else:
        bot.action(f'gives {trigger.group(2)} a present.', trigger.sender)


@example('.hotchoc MirahezeBot')
@commands('hotchoc', 'hotchocolate')
def hotchoc(bot, trigger):
    """Make me give the specified nick a hot chocolate."""
    if trigger.group(2) is None:
        bot.reply('To whom should I give this hot chocolate?')
    else:
        bot.action(f'gives {trigger.group(2)} a warm, velvety salted caramel hot chocolate with cream and marhsmellows.',
                   trigger.sender)
