from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands, example



@commands('miraheze')
@example('.miraheze')
def miraheze(bot, trigger):
	"""
Miraheze about command

This command will tell you about Miraheze and where to learn more 
	"""
	if trigger.sender == '#miraheze':
		bot.say(trigger.nick + ', Miraheze is a non-profit wikifarm running MediaWiki. If you would like more information please see, https://meta.miraheze.org/ or ask in this channel.')
	else:
		bot.say(trigger.nick + ', Miraheze is a non-profit wikifarm running MediaWiki. If you would like more information please see, https://meta.miraheze.org/ or #miraheze.')
@commands('gethelp')
@example('.gethelp I cannot access https://www.meta.miraheze.org')
def mirahezegehelp(bot, trigger):
	bot.say(trigger.nick + ', needs help. Pinging Reception123, Zppix, PuppyKun, Voidwalker.')
@commands('dns', 'ns', 'nameservers')
def mhdns(bot, trigger):
"""
Information about how Miraheze handles DNS/Nameservers
"""
	bot.say(trigger.nick + ': Miraheze, once gaven any and all info applicable to getting your domain setup (including DNS and/or other nameservers), it will take up to 48 hours. However, this process will only start once the DNS patch has been merged. For more information, please feel free to ask')
