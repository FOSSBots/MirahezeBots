"""phab.by - Phabricator Task Information Plugin"""

from sopel.module import commands, example, interval, rule
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
        bot.say(phabsearch.searchphab(PHAB_SETTINGS[trigger.sender], task=task_id), trigger.sender)
    except AttributeError:
        bot.say('Syntax: .task (task ID with or without T)', trigger.sender)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = (trigger.match.group(0)).split('T')[1]
    bot.say(phabsearch.searchphab(PHAB_SETTINGS[trigger.sender], task=task_id), trigger.sender)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    if bot.settings.phabricator.highpri_notify is True:
        """Send high priority tasks notifications."""
        bot.say(phabsearch.gethighpri(PHAB_SETTINGS[trigger.sender]), trigger.sender)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    bot.say(gethighpri(PHAB_SETTINGS[trigger.sender], limit=False), trigger.sender) # will need changing
