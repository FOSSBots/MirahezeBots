from sopel.module import rule

@rule('update.php')
def ping_converse(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Oh no, update.php! If you're not upgrading MediaWiki, you should really not be using that!")
 
