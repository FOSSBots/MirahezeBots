from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands, example

@commands('botversion','bv')
@example('.botversion')
 def adminlist(bot, trigger):
   """
  Lists the current version of the bot
   """
   bot.say('The current version of this bot is 2.0 (v2)')
