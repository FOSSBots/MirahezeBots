"""This module implements channel joining on startup to fix a bug."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

from sopel import module

import time

chans = ['#miraheze-cvt', '#testadminwiki', '#miraheze-testwiki-es',
         '#miraheze', '#miraheze-testwiki', '#miraheze-cvt-private',
         '##CyberBogan', '##RhinosF1', '##acme', '#miraheze-offtopic',
         '#ays']


@module.require_admin
@module.commands('joinall')
@module.thread(True)
def handle_joins(bot, trigger):
    """Join some channels."""
    if trigger.sender == '#ZppixBot':
        for chan in chans:
            bot.join(chan)
            time.sleep(1)


@module.rule('.*')
@module.event('JOIN')
@module.thread(True)
@module.unblockable
def handle_joins_auto(bot, trigger):
    """Join some channels automatically."""
    if trigger.nick == bot.nick and trigger.sender == '#ZppixBot':
        for chan in chans:
            bot.join(chan)
            time.sleep(1)
