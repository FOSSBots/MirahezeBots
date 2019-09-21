# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division

import os
import sopel
import sopel.module
import sopel.tools

from sopel.module import commands, require_admin

@commands('testing')
@require_admin
def tests(bot, trigger):
    """Perform tests on the bot. May change or be remove without notice."""
    if bot.config.ip.GeoIP_db_path:
        bot.reply(bot.config.ip.GeoIP_db_path)
        if os.path.isfile(os.join(bot.config.ip.GeoIP_db_path, 'GeoLite2-City.mmdb')):
            bot.say('And a file exists there too!')
        else:
            bot.say('But no file seems to exist!')
    elif bot.config.core.homedir:
        bot.reply(bot.config.core.homedir)
        if os.path.isfile(os.path.join(bot.config.core.homedir, 'GeoLite2-City.mmdb')):
            bot.say('And a file exists there too!')
        else:
            bot.say('But no file seems to exist!')
    else:
        bot.reply('/usr/share/GeoIP')
