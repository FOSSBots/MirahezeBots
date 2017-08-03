from sopel.module import rule

@rule('update.php')
def ping_converse(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Oh no, update.php! If you're not upgrading MediaWiki, you should really not be using that!")
@rule('my wiki is down', 'Miraheze is down')
def ping_converse(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Oh no! That sounds bad. A sysadmin should be here shortly to investigate. If you haven't, please file a Phabricator ticket to facilitate the process!")                
 
