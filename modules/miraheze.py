from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands


@commands('miraheze')
def miraheze(bot, trigger):
    bot.say(' ' + trigger.nick + ' Miraheze is a non-profit wikifarm running MediaWiki. If you would like more information please see, https://meta.miraheze.org/ or #miraheze.')

