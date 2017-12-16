from sopel.module import rule

@rule('.*$nickname.*')
def ping_converse(bot, trigger):
    if trigger.nick == 'Reception123':
        bot.say("I get it, Reception123, you want to talk to someone, but you shouldn't pick a dumb AI like me, talk to an actual person.")
    elif trigger.nick == 'Reception|away':
        bot.say("I get it, Reception123, you want to talk to someone, but you shouldn't pick a dumb AI like me, talk to an actual person.")
    elif trigger.nick == 'PuppyKun':
        bot.say("Hit the tab button too soon again, PuppyKun? Tsk tsk tsk.")
    elif trigger.nick == 'wm-bot' or trigger.nick == 'wm-bot2' or trigger.nick == 'wm-bot3' or trigger.nick == 'Source-Zppixbot' or trigger.nick == 'wikibugs' or trigger.sender == '#wiki-dev-africa' or trigger.nick == 'wikibugs_':
        return  
    elif trigger.nick == 'Zppix':
        bot.say("Talking to your own AI bot again, are you Zppix?")
    else:
        bot.say("Hey, %s, I'm an AI which is too dumb to carry on a converstation perhaps, you meant to ping Zppix instead?" % trigger.nick)
