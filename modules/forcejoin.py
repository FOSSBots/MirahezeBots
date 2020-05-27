"""On Command joinall Channel Please Htnak You script - forces the bot to join all channels"""  # for sopel devs

from sopel import module, config

import time

chans = config.channels().split('
                               ')


@module.require_admin
@module.commands('joinall')
@module.thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    if trigger.sender == '#ZppixBot':
        for chan in chans:
            bot.join(chan)
            time.sleep(2)
