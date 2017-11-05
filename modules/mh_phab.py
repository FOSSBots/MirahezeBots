from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands, example

@commands('task')
@example('.task 1')
"""Get a Miraheze phabricator link to a the task number you provide."""
def phabtask(bot, trigger):
    bot.say('https://phabricator.miraheze.org/T'+ trigger.group(2))
