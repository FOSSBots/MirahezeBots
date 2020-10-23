"""phab.by - Phabricator Task Information Plugin"""

import requests  # FIX THIS
from sopel.module import commands, example, interval, rule, require_admin
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute
from json import JSONDecodeError
from urllib.parse import urlparse
from MirahezeBots.utils import phabsearch


def setup(bot):
    PHAB_SETTINGS = bot.memory["settings"]["phab"]


BOLD = '\x02'
HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    try:
        if trigger.group(2).startswith('T'):
            task_id = trigger.group(2).split('T')[1]
        else:
            task_id = trigger.group(2)
        phabsearch.searchphab(bot=bot, channel=trigger.sender, task=task_id)
    except AttributeError:
        bot.say('Syntax: .task (task ID with or without T)', trigger.sender)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = (trigger.match.group(0)).split('T')[1]
    phabsearch.searchphab(bot=bot, channel=trigger.sender, task=task_id)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    if bot.settings.phabricator.highpri_notify is True:
        """Send high priority tasks notifications."""
        phabsearch.gethighpri(channel=bot.settings.phabricator.highpri_channel, bot=bot)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    gethighpri(limit=False, channel=trigger.sender, bot=bot)
