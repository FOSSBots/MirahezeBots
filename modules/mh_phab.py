"""This module contains commands related to Miraheze Phabricator."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

import sys
import os
import re

from sopel.module import commands, example

# sopel modules import problem workaround
sys.path.insert(0, os.path.abspath(__file__ + "/.."))
from utils.phabricator import PhabricatorClient


def setup(bot):
    """Setup phabricator client."""
    if hasattr(bot.config, 'phabricator'):
        bot.phabricator = PhabricatorClient(
            bot.config.phabricator.host,
            bot.config.phabricator.api_token
        )


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = int(re.sub("[^0-9]", "", trigger.group(2)))

    if not hasattr(bot, 'phabricator'):
        # Fallback for case if phabricator is not set up
        bot.say('https://phabricator.miraheze.org/T{}'.format(task_id))
        return

    task = bot.phabricator.get_task(task_id)

    if task is None:
        bot.reply('I can\'t find task with id {}'.format(task_id))
        return

    message = '{} - {} [{}] authored by {}'.format(
        task.link,
        task.title,
        task.status,
        task.author.username
    )
    if task.owner is not None:
        message += ', assigned to {}'.format(task.owner.username)
    else:
        message += ', assigned to None'
    bot.say(message)
