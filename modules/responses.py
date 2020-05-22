"""This module sends responses to frequently posted messages at #miraheze."""

from sopel.module import commands, example
import platform


@commands('addchannel')
@example('.addchannel (insert which)')
def addchan(bot, trigger):
    """Reply to channel request message."""
    bot.say(("Hey Voidwalker, Reception123 or Zppix, {} would like to have "
            + "me in their channel: {}").format(trigger.nick, trigger.group(2)),
            '#ZppixBot')
    if trigger.sender != '#ZppixBot':
        bot.reply("Request sent! Action upon the request should be taken shortly. Thank you for using ZppixBot!")


@commands('gj', 'gw')
@example('.gj (nick)')
def gj(bot, trigger):
    """Tell the user that they are doing good work."""
    bot.say(("You're doing good work, {}!").format(trigger.group(2)))


@commands('cancelreminder')
@example('.cancelreminder (insert reminder message here)')
def cancel(bot, trigger):
    """Cancel reminder."""
    bot.reply(('Pinging RhinosF1, Reception123, Voidwalker or Zppix to cancel '
               '{}\'s reminder.').format(trigger.nick))


@commands('botversion', 'bv')
@example('.botversion')
def botversion(bot, trigger):
    """List the current version of the bot."""
    bot.say('The current version of this bot is 6.0 (v6)')


@commands('source', 'botsource')
@example('.source')
def githubsource(bot, trigger):
    """Give the link to ZppixBot's Github."""
    bot.reply('My code can be found here: https://github.com/Pix1234/ZppixBot-Source')


@commands('python', 'pyver')
def pythonversion(bot, trigger):
    """Reply with Python version bot is running."""
    bot.say("I am running Python " + platform.python_version() + ".")
