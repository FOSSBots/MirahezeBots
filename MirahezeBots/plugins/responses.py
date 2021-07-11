"""responses.py - like a FAQ bot."""

from sopel import bot, trigger, config
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.plugin import commands, example, rate, require_account

from MirahezeBots.version import SHORTVERSION, VERSION


class ResponsesSection(StaticSection):
    """Create configuration for Sopel."""

    support_channel = ValidatedAttribute('support_channel', str)


def setup(instance: bot) -> None:
    """Set up the config section."""
    instance.config.define_section('responses', ResponsesSection)


def configure(config: config) -> None:
    """Set up the configuration options."""
    config.define_section('responses', ResponsesSection, validate=False)
    config.responses.configure_setting('support_channel', 'Specify a support IRC channel (leave blank for none).')


@commands('addchannel')
@example('.addchannel (insert which)')
@rate(user=120, channel=240, server=60)
@require_account()
def addchan(instance: bot, message: trigger) -> None:
    """Reply to channel request message."""
    admins = ' '.join(map(str, instance.config.core.admin_accounts))
    if instance.config.responses.support_channel is not None:
        instance.say(
            f'Hey {admins}, {message.nick} would like to have me in their channel: {message.group(2)}',
            instance.config.responses.support_channel,
        )
        if message.sender != instance.config.responses.support_channel:
            instance.reply(f'Request sent! Action upon the request should be taken shortly. Thank you for using {instance.nick}!')


@commands('gj', 'gw')
@example('.gj (nick)')
@rate(user=2, channel=1, server=0)
def gj(instance: bot, message: trigger) -> None:
    """Tell the user that they are doing good work."""
    instance.say(f"You're doing good work, {message.group(2)}!")


@commands('cancelreminder')
@example('.cancelreminder (insert reminder message here)')
@rate(user=2, channel=1, server=0)
def cancel(instance: bot, message: trigger) -> None:
    """Cancel reminder."""
    admins = ' '.join(map(str, instance.config.core.admin_accounts))
    instance.reply(f"Pinging {admins} to cancel {message.nicks}'s reminder.")


@commands('botversion', 'bv')
@example('.botversion')
@rate(user=2, channel=1, server=0)
def botversion(instance: bot, message: trigger) -> None:  # noqa: U100
    """List the current version of the bot."""
    instance.reply(f'The current version of this bot is {VERSION} ({SHORTVERSION})')


@commands('source', 'botsource')
@example('.source')
@rate(user=2, channel=1, server=0)
def githubsource(instance: bot, message: trigger) -> None:  # noqa: U100
    """Give the link to MirahezeBot's Github."""
    instance.reply('My code can be found here: https://github.com/MirahezeBots/MirahezeBots')
