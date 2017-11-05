from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands, example

@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    bot.say('https://phabricator.miraheze.org/T'+ trigger.group(2))
