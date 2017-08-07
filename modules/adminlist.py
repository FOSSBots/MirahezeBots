from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands, example

@commands('botadmins','admins')
@example('.admins')
 def adminlist(bot, trigger):
   """
  Lists the current bot admins
   """
  if trigger.nick == 'Reception123' or trigger.nick == 'Reception|away':
    bot.say(trigger.nick + ', the bot\'s admins are: You, SwisterTwister and Zppix.')
  elif trigger.nick == 'Zppix':
    bot.say(trigger.nick + ', the bot\'s admins are: Reception123, SwisterTwister and you.')
  elif trigger.nick == 'SwisterTwister' or trigger.nick == 'StormyWaves':
    bot.say(trigger.nick + ', the bot\'s admins are: Reception123, You and Zppix.')
  else:
    bot.say(trigger.nick + ', the bot\'s admins are: Reception123, SwisterTwister and Zppix.')
@commands('accesslevel')
@example('.accesslevel')
def accesslevel(bot,trigger):
     """
    Finds the accesslevel of the user executing the command
     """
  if trigger.nick  == 'Reception123' or trigger.nick == 'Reception|away':
    bot.say('The access level for ' + trigger.nick + ', is Admin.')
  elif trigger.nick == 'Zppix':
      bot.say('The access level for ' + trigger.nick + ', is Owner.')
  elif trigger.nick == 'SwisterTwister' or trigger.nick == 'StormyWaves':
        bot.say('The access level for ' + trigger.nick + ', is Admin.')
  else:
          bot.say('The access level for ' + trigger.nick + ', is User.')
