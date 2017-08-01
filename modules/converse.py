from sopel.module import rule

@rule('.*$nickname.*')
def ping_converse(bot, trigger):
    bot.say("Hey, %s, I'm an AI which is to dumb to carry on a converstation perhaps, you meant to ping Zppix instead?" % trigger.nick)
