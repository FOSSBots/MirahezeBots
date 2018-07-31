"""This module sends responses to frequently posted messages at #miraheze."""

from sopel.module import rule, commands, example


@commands('addchannel')
@example('.addchannel (insert which)')
def cancel(bot, trigger):
    """Reply to channel request message."""
    bot.reply(("Hey MacFan4000, Reception123 or Zppix, {} would like to have "
               "me in their channel").format(trigger.nick))


@rule('update.php')
def ping_converse(bot, trigger):
        """Reply to message specified in rule."""
        if trigger.sender == '#miraheze':
                bot.say("Oh no, update.php! If you're not upgrading MediaWiki,"
                        " you should really not be using that!")


@rule('my wiki is down')
def ping_converse2(bot, trigger):
        """Reply to message specified in rule."""
        if trigger.sender == '#miraheze':
                bot.say("That sounds bad. A sysadmin should be here shortly to"
                        " investigate. If you haven't already, please file a "
                        "Phabricator ticket to facilitate the process!")


@rule('Miraheze is down')
def ping_converse3(bot, trigger):
        """Reply to message specified in rule."""
        if trigger.sender == '#miraheze':
                bot.say("That sounds bad! A sysadmin should be here shortly to"
                        " investigate. If you haven't already, please file a "
                        "Phabricator ticket to facilitate the process!")


@rule('getting 503')
def ping_converse4(bot, trigger):
        """Reply to message specified in rule."""
        if trigger.sender == '#miraheze' and trigger.nick != 'icinga-miraheze':
                bot.reply("The servers should return back to normal shortly."
                          "If that is not the case, please file a task on "
                          "Phabricator immediately")


@rule('The upgrade was successful')
def ping_converse5(bot, trigger):
        """Reply to message specified in rule."""
        if trigger.sender == '#miraheze':
                bot.say("Good job %s! Keep on doing what you do.")


@rule('Thanks ZppixBot')
def ping_converse6(bot, trigger):
        """Reply to message specified in rule."""
        if trigger.sender == '#miraheze':
                bot.say('You\'re welcome ' + trigger.nick)


@rule('Hi ZppixBot')
def ping_converse7(bot, trigger):
        """Reply to message specified in rule."""
                bot.say('Hi ' + trigger.nick + '. Do you need anything from me?')
