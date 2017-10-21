from sopel import module

@commands('task', 't')
def phabtask(bot, trigger):
    bot.say('https://www.phabricator.miraheze.org/'+ trigger.group(2))
