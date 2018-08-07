"""This module provides information about bot version."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel.module import commands, example


@commands('botversion', 'bv')
@example('.botversion')
def botversion(bot, trigger):
    """List the current version of the bot."""
    bot.say('The current version of this bot is 3.0 (v3)')
    
@commands('source', 'botsource')
@example('.source')
def githubsource(bot,trigger):
    """Give the link to ZppixBot's Github."""
    bot.reply('My code can be found here: https://github.com/Pix1234/ZppixBot-Source')
