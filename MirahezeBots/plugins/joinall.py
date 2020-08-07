"""This module implements .joinall."""

from sopel import module

import time


@module.require_admin
@module.commands('joinall')
@module.thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    channels = bot.config.core.channels
    for channel in channels:
        bot.join(channel)
        time.sleep(1)
