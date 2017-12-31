"""This module replies to some messages specified by regular expressions."""

from sopel.module import rule


@rule('.*$nickname.*')
def ping_converse(bot, trigger):
    """Reply to messages containing this bot name."""
    if trigger.nick in ['Reception123', 'Reception|away']:
        bot.say("I get it, Reception123, you want to talk to someone,"
                "but you shouldn't pick a dumb AI like me, talk to an actual"
                " person.")
    else:
        return


@rule('.*request.*wiki.*')
def reply_to_wiki_request(bot, trigger):
    """Reply to wiki request messages in #miraheze."""
    if trigger.nick == 'Not-144f':
        return
    elif trigger.sender == '#miraheze':
        bot.reply("To request a wiki, please see "
                  "https://meta.miraheze.org/wiki/Special:RequestWiki")
