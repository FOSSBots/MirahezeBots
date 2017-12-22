from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands

@commands('botadmins','admins')
def adminlist(bot, trigger):
  if trigger.nick == 'Reception123':
    bot.say(trigger.nick + ', the bot\'s admins are: paladox, You, MacFan400, SwisterTwister and Zppix.')
  elif trigger.nick == 'Zppix':
    bot.say(trigger.nick + ', the bot\'s admins are: paladox, Reception123, SwisterTwister and you.')
  elif trigger.nick == 'SwisterTwister':
    bot.say(trigger.nick + ', the bot\'s admins are: paladox, Reception123, MacFan400, You and Zppix.')
  elif trigger.nick == 'paladox':
    bot.say(trigger.nick + ', the bot\'s admins are: You, Reception123, SwisterTwister, MacFan400 and Zppix.')
  elif trigger.nick == 'MacFan400':
    bot.say(trigger.nick + ', the bot\'s admins are: paladox, Reception123, SwisterTwister, You, and Zppix.')
  else:
    bot.say(trigger.nick + ', the bot\'s admins are: paladox, Reception123, SwisterTwister, MacFan400 and Zppix.')
@commands('accesslevel')
def accesslevel(bot,trigger):
  if trigger.nick  == 'Reception123':
    bot.say('The access level for ' + trigger.nick + ', is Admin.')
  elif trigger.nick == 'Zppix':
      bot.say('The access level for ' + trigger.nick + ', is Owner.')
  elif trigger.nick == 'SwisterTwister':
        bot.say('The access level for ' + trigger.nick + ', is Admin.')
  elif trigger.nick == 'paladox' or trigger.nick == 'MacFan400':
        bot.say('The access level for ' + trigger.nick + ', is Admin.')
  else:
          bot.say('The access level for ' + trigger.nick + ', is User.')
