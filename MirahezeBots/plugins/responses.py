"""responses.py - like a FAQ bot"""

from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example, rate, require_account

from MirahezeBots.version import VERSION, SHORTVERSION


class ResponsesSection(StaticSection):
    support_channel = ValidatedAttribute('support_channel', str)


def setup(bot):
    bot.config.define_section('responses', ResponsesSection)


def configure(config):
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
        bot.say(("Hey {}, {} would like to have me in their channel: {}").format(admins, trigger.nick, trigger.group(2)),
                bot.config.responses.support_channel)
        if trigger.sender != bot.config.responses.support_channel:
            bot.reply("Request sent! Action upon the request should be taken shortly. Thank you for using {}!".format(bot.nick))


@commands('gj', 'gw')
@example('.gj (nick)')
@rate(user=2, channel=1, server=0)
def gj(bot, trigger):
    """Tell the user that they are doing good work."""
    bot.say(("You're doing good work, {}!").format(trigger.group(2)))


@commands('cancelreminder')
@example('.cancelreminder (insert reminder message here)')
@rate(user=2, channel=1, server=0)
def cancel(bot, trigger):
    """Cancel reminder."""
    admins = ' '.join(map(str, bot.config.core.admin_accounts))
    bot.reply(('Pinging {} to cancel '
               '{}\'s reminder.').format(admins, trigger.nick))


@commands('botversion', 'bv')
@example('.botversion')
@rate(user=2, channel=1, server=0)
def botversion(bot, trigger):
    """List the current version of the bot."""
    bot.say('The current version of this bot is {} ({})'.format(VERSION, SHORTVERSION))


@commands('source', 'botsource')
@example('.source')
@rate(user=2, channel=1, server=0)
def githubsource(bot, trigger):
    """Give the link to MirahezeBot's Github."""
    bot.reply('My code can be found here: https://github.com/MirahezeBots/MirahezeBots')
