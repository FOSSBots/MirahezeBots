from sopel.module import rule

@rule('.*$nickname.*')
def ping_converse(bot, trigger):
    if trigger.nick == 'Reception123':
        bot.say("I get it, Reception123, you want to talk to someone, but you shouldn't pick a dumb AI like me, talk to an actual person.")
    elif trigger.nick == 'Reception|away':
        bot.say("I get it, Reception123, you want to talk to someone, but you shouldn't pick a dumb AI like me, talk to an actual person.")
    else:
        return

@rule('.*request.*wiki.*')
def ping_miraheze (bot, trigger):
   if trigger.nick == 'Not-e084':
    return
   elif trigger.sender == '#miraheze':
    bot.reply("To request a wiki, please see https://meta.miraheze.org/wiki/Special:RequestWiki")
