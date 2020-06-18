"""This module sends responses to frequently posted messages at #miraheze."""

from sopel.module import commands, example, rate, require_account


@commands('addchannel')
@example('.addchannel (insert which)')
@rate(user=120, channel=240, server=60)
@require_account()
def addchan(bot, trigger):
    """Reply to channel request message."""
    bot.say(("Hey MacFan4000, RhinosF1, Texas, Voidwalker, Reception123 or Zppix, {} would like to have "
            + "me in their channel: {}").format(trigger.nick, trigger.group(2)),
            '#ZppixBot')
    if trigger.sender != '#ZppixBot':
        bot.reply("Request sent! Action upon the request should be taken shortly. Thank you for using ZppixBot!")


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
    bot.reply(('Pinging RhinosF1, Reception123, Voidwalker or Zppix to cancel '
               '{}\'s reminder.').format(trigger.nick))


@commands('botversion', 'bv')
@example('.botversion')
@rate(user=2, channel=1, server=0)
def botversion(bot, trigger):
    """List the current version of the bot."""
    bot.say('The current version of this bot is 6.0 (v6)')


@commands('source', 'botsource')
@example('.source')
@rate(user=2, channel=1, server=0)
def githubsource(bot, trigger):
    """Give the link to ZppixBot's Github."""
    bot.reply('My code can be found here: https://github.com/Pix1234/ZppixBot-Source')
