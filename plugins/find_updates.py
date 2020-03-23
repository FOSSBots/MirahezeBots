# coding=utf-8
"""Update checking module for Sopel.

This is separated from version.py, so that it can be easily overridden by
distribution packagers, and they can check their repositories rather than the
Sopel website.
"""
# Copyright 2014, Elsie Powell, embolalia.com
# Licensed under the Eiffel Forum License 2.
from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

import sopel
import sopel.plugin
import requests
import sopel.tools

wait_time = 24 * 60 * 60  # check once per day
startup_check_run = False
version_url = 'http://sopel.chat/latest.json'
message = (
    'A new Sopel version, {}, is available. I am running {}. Please update '
    'me. Full release notes at {}'
)
unstable_message = (
    'A new pre-release version, {}, is available. I am running {}. Please '
    'update me. {}'
)


@sopel.module.event(sopel.tools.events.RPL_LUSERCLIENT)
@sopel.module.rule('.*')
def startup_version_check(bot, trigger):
    """Check sopel version on startup."""
    global startup_check_run
    if not startup_check_run:
        startup_check_run = True
        check_version(bot)


@sopel.module.interval(wait_time)
def check_version(bot):
    """Check latest sopel version. Notify bot owner if there is an update."""
    version = sopel.version_info

    info = requests.get(version_url).json()
    if version.releaselevel == 'final':
        latest = info['version']
        notes = info['release_notes']
    else:
        latest = info['unstable']
        notes = info.get('unstable_notes', '')
        if notes:
            notes = 'Full release notes at ' + notes
    latest_version = sopel._version_info(latest)
    msg = message.format(latest, sopel.__version__, notes)

    if version < latest_version:
        bot.say(msg, bot.config.core.owner)
