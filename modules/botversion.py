"""This module provides information about bot version."""

from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import commands, example


@commands('botversion', 'bv')
@example('.botversion')
def botversion(bot):
    """List the current version of the bot."""
    bot.say('The current version of this bot is 3.0 (v3)')
