"""responses.py - like a FAQ bot."""

from MirahezeBots.version import SHORTVERSION, VERSION

from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example, rate, require_account


class ResponsesSection(StaticSection):
    """Create configuration for Sopel."""

    support_channel = ValidatedAttribute('support_channel', str)


def setup(bot):
    """Set up the config section."""
    bot.config.define_section('responses', ResponsesSection)


def configure(config):
    """Set up the configuration options."""
    config.define_section('responses', ResponsesSection, validate=False)
    config.responses.configure_setting('support_channel', 'Specify a support IRC channel (leave blank for none).')


@commands('addchannel')
@example('.addchannel (insert which)')
@rate(user=120, channel=240, server=60)
@require_account()
def addchan(bot, trigger):
    """Reply to channel request message."""
    admins = ' '.join(map(str, bot.config.core.admin_accounts))
    if bot.config.responses.support_channel is not None:
        bot.say(f'Hey {admins}, {trigger.nick} would like to have me in their channel: {trigger.group(2)}',
                bot.config.responses.support_channel)
        if trigger.sender != bot.config.responses.support_channel:
            bot.reply(f'Request sent! Action upon the request should be taken shortly. Thank you for using {bot.nick}!')


@commands('gj', 'gw')
@example('.gj (nick)')
@rate(user=2, channel=1, server=0)
def gj(bot, trigger):
    """Tell the user that they are doing good work."""
    bot.say(f"You're doing good work, {trigger.group(2)}!")


@commands('cancelreminder')
@example('.cancelreminder (insert reminder message here)')
@rate(user=2, channel=1, server=0)
def cancel(bot, trigger):
    """Cancel reminder."""
    admins = ' '.join(map(str, bot.config.core.admin_accounts))
    bot.reply(f"Pinging {admins} to cancel {trigger.nicks}'s reminder.")


@commands('botversion', 'bv')
@example('.botversion')
@rate(user=2, channel=1, server=0)
def botversion(bot, trigger):  # noqa: U100
    """List the current version of the bot."""
    bot.reply(f'The current version of this bot is {VERSION} ({SHORTVERSION})')


@commands('source', 'botsource')
@example('.source')
@rate(user=2, channel=1, server=0)
def githubsource(bot, trigger):  # noqa: U100
    """Give the link to MirahezeBot's Github."""
    bot.reply('My code can be found here: https://github.com/MirahezeBots/MirahezeBots')
