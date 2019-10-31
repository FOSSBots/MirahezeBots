"""This module implements channel joining on startup to fix a bug."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel.module import (event, thread)

import time


@event('JOIN')
@thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    if trigger.nick == bot.nick and trigger.sender == '#ZppixBot':
        chans = ['#miraheze-cvt', '#testadminwiki', '#miraheze-testwiki-es',
                 '#miraheze', '#miraheze-testwiki', '#miraheze-cvt-private',
                 '##CyberBogan', '##RhinosF1', '##acme', '#miraheze-offtopic',
                 '#ays']
        for chan in chans:
            bot.join(chan)
            time.sleep(1)
