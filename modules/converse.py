"""This module replies to some messages specified by regular expressions."""

from sopel.module import rule


@rule('.*change.*logo.*')
def reply_to_logo_change__request(bot, trigger):
    """Reply to logo change messages in #miraheze."""
    if trigger.nick == 'Not-144f':
        return
    elif trigger.sender == '#miraheze':
        bot.reply("To change the logo for your wiki, please request "
                  "at the following link: https://phabricator.miraheze.org/maniphest/task/edit/form/7/")
