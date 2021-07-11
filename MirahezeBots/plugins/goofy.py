"""Some commands for just goofing around and having fun."""

from sopel.plugin import commands, example
from sopel import bot, trigger


@example('.coffee MirahezeBot')
@commands('coffee')
def coffee(instance: bot, message: trigger) -> None:
    """Make me give the specified nick a coffee."""
    if message.group(2) is None:
        instance.reply('To whom should I give this cup of coffee?')
    else:
        instance.action(f'gives {message.group(2)} a nice warm cup of coffee.', message.sender)


@example('.hug MirahezeBot')
@commands('hug')
def hug(instance: bot, message: trigger) -> None:
    """Make me give the specified nick a hug."""
    if message.group(2) is None:
        instance.reply('To whom should I give this hug?')
    else:
        instance.action(f'gives {message.group(2)} a great big bear hug.', message.sender)


@example('.burger MirahezeBot')
@commands('burger')
def burger(instance: bot, message: trigger) -> None:
    """Make me give the specified nick a burger."""
    if message.group(2) is None:
        instance.reply('To whom should I give this cheeseburger?')
    else:
        instance.action(f'gives {message.group(2)} a freshly cooked cheeseburger.', message.sender)


@example('.present MirahezeBot')
@commands('present')
def present(instance: bot, message: trigger) -> None:
    """Make me give the specified nick a present."""
    if message.group(2) is None:
        instance.reply('To whom should I give this present?')
    else:
        instance.action(f'gives {message.group(2)} a present.', message.sender)


@example('.hotchoc MirahezeBot')
@commands('hotchoc', 'hotchocolate')
def hotchoc(instance: bot, message: trigger) -> None:
    """Make me give the specified nick a hot chocolate."""
    if message.group(2) is None:
        instance.reply('To whom should I give this hot chocolate?')
    else:
        instance.action(
            f'gives {message.group(2)} a warm, velvety salted caramel hot chocolate with cream and marhsmellows.',
            message.sender,
        )
