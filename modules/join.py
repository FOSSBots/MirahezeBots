"""This module implements channel joining on startup to fix a bug."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel.module import (commands, thread, require_admin)

import time


@require_admin
@commands('joinall')
@thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    if trigger.sender == '#ZppixBot':
        chans = ['#miraheze-cvt', '#testadminwiki', '#miraheze-testwiki-es',
                 '#miraheze', '#miraheze-testwiki', '#miraheze-cvt-private',
                 '##CyberBogan', '##RhinosF1', '##acme', '#miraheze-offtopic',
                 '#ays']
        for chan in chans:
            bot.join(chan)
            time.sleep(1)
