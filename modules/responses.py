from sopel.module import rule

@rule('update.php')
def ping_converse(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Oh no, update.php! If you're not upgrading MediaWiki, you should really not be using that!")
@rule('my wiki is down')
def ping_converse2(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Oh no! That sounds bad. A sysadmin should be here shortly to investigate. If you haven't already, please file a Phabricator ticket to facilitate the process!")                
@rule('Miraheze is down')
def ping_converse3(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("That sounds bad! A sysadmin should be here shortly to investigate. If you haven't already, please file a Phabricator ticket to facilitate the process!")
