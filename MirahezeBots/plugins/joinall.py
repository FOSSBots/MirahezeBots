"""This plugin implements .joinall."""

import time

from sopel.module import commands, require_admin, thread


@require_admin
@commands('joinall')
@thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    channels = bot.config.core.channels
    for channel in channels:
        bot.join(channel)
        time.sleep(1)
