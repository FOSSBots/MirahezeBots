"""This module replies to some messages specified by regular expressions."""

from sopel.module import rule


@rule('.*request.*wiki.*')
def reply_to_wiki_request(bot, trigger):
    """Reply to wiki request messages in #miraheze."""
    if trigger.nick == 'Not-144f':
        return
    elif trigger.sender == '#miraheze':
        bot.reply("To request a wiki, please see "
                  "https://meta.miraheze.org/wiki/Special:RequestWiki")
