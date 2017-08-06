from sopel.module import rule

@rule('update.php')
def ping_converse(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Oh no, update.php! If you're not upgrading MediaWiki, you should really not be using that!")
@rule('my wiki is down')
def ping_converse2(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("That sounds bad. A sysadmin should be here shortly to investigate. If you haven't already, please file a Phabricator ticket to facilitate the process!")                
@rule('Miraheze is down')
def ping_converse3(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("That sounds bad! A sysadmin should be here shortly to investigate. If you haven't already, please file a Phabricator ticket to facilitate the process!")
@rule('The upgrade was successful')
def ping_converse4(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.say("Good job %s! Keep on doing what you do.")
@rule('[dns] Reception123 opened pull request')
def ping_converse5(bot, trigger):
        if trigger.sender == '#miraheze':
                bot.tell("12h PuppyKun: Please don't forget to merge a DNS PR started by Reception123.")
                
               
