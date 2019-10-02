"""This module sends responses to frequently posted messages at #miraheze."""

from sopel.module import rule, commands, example


@commands('addchannel')
@example('.addchannel (insert which)')
def cancel(bot, trigger):
    """Reply to channel request message."""
    bot.reply(("Hey Voidwalker, Reception123 or Zppix, {} would like to have "
               "me in their channel").format(trigger.nick))


@commands('gj', 'gw')
@example('.gj (nick)')
def cancel2(bot, trigger):
    """tell the user that they are doing good work."""
    bot.say(("You're doing good work, {}!").format(trigger.group(2)))
