"""This module expands links to various websites"""

from sopel.module import rule, commands, example


@commands('github')
@example('.github repo')
def cancel2(bot, trigger):
    bot.say(("https://github.com/{}").format(trigger.group(2)))
