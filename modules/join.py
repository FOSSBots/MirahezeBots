"""This module implements channel joining on startup to fix a bug."""

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


@module.rule('.*')
@module.event('JOIN')
@module.thread(True)
@module.unblockable
def handle_joins_auto(bot, trigger):
    """Join some channels automatically."""
    channels = bot.config.core.channels
    if trigger.nick == bot.nick and trigger.sender == '#ZppixBot':
        for channel in channels:
            bot.join(channel)
            time.sleep(1)
