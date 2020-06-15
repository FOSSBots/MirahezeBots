"""This module implements .joinall."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel import module

import time


@module.require_admin
@module.commands('joinall')
@module.thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    channels = bot.config.core.channels
    if trigger.sender == '#ZppixBot':
        for channel in channels:
            bot.join(channel)
            time.sleep(1)
