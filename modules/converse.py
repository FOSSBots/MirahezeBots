from sopel.module import rule

@rule('.*$nickname.*')
def ping_converse(bot, trigger):
if trigger.nick == 'Reception123' or trigger.nick == 'Reception|away':
    bot.say("I get it, Reception123, talking to real people is too overrated." % trigger.nick)
elif trigger.nick == 'PuppyKun':
    bot.say("Hit the tab button too soon again, PuppyKun? Tsk tsk tsk." % trigger.nick)
elif trigger.nick == 'Zppix':
    bot.say("Talking to your own AI bot again, are you Zppix?" % trigger.nick)
else:
    bot.say("Hey, %s, I'm an AI which is to dumb to carry on a converstation perhaps, you meant to ping Zppix instead?" % trigger.nick)
