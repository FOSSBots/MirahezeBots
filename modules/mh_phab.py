from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands

@commands('task')
def phabtask(bot, trigger):
    bot.say('https://www.phabricator.miraheze.org/T'+ trigger.group(2))
