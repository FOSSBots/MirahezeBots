from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands

@commands('botadmins','admins')
def adminlist(bot, trigger):
  bot.say(trigger.nick + ', the bot's admins are: Reception123, SwisterTwister and Zppix.')
