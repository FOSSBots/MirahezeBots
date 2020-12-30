"""phab.by - Phabricator Task Information Plugin."""

from MirahezeBots.utils import phabapi

from MirahezeBots_jsonparser import jsonparser as jp

from sopel.config.types import ListAttribute, StaticSection, ValidatedAttribute
from sopel.module import commands, example, interval, require_admin, rule
from sopel.tools import SopelMemory



BOLD = '\x02'
HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []


def get_host_and_api_or_query_key(channel, cache, keys):
    """Get hostname,apikey and querykey for instance."""
    if channel in cache:
        host = cache[str(channel)]["host"]
        arraypos = int(cache[str(host)]["arraypos"])
        apikey = keys[0][int(arraypos)]
        querykey = keys[1][int(arraypos)]
    else:
        host = cache["default"]["host"]
        arraypos = int(cache[str(host)]["arraypos"])
        apikey = keys[0][int(arraypos)]
        querykey = keys[1][int(arraypos)]
    return host, apikey, querykey


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    """Get information on a phabricator task."""
    try:
        if trigger.group(2).startswith('T'):
            task_id = trigger.group(2).split('T')[1]
        else:
            task_id = trigger.group(2)
        info = get_host_and_api_or_query_key(trigger.sender, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])
        bot.reply(phabapi.gettaskinfo(info[0], info[1], task=task_id))
    except AttributeError:
        bot.say('Syntax: .task (task ID with or without T)', trigger.sender)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = (trigger.match.group(0)).split('T')[1]
    info = get_host_and_api_or_query_key(trigger.sender, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send regular update on high priority tasks."""
    if bot.settings.phabricator.highpri_notify is True:
        """Send high priority tasks notifications."""
        info = get_host_and_api_or_query_key(bot.settings.phabricator.highpri_channel, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])
        result = phabapi.dophabsearch(info[0], info[1], info[2])
        if result:
            bot.say("Your weekly high priority task update:", bot.settings.phabricator.highpri_channel)
            for task in result:
                bot.say(task, bot.settings.phabricator.highpri_channel)
        else:
            bot.say("High priority task update: Tasks exceeded limit or could not be found. Use \".highpri\"", bot.settings.phabricator.highpri_channel)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    """Send full list of high priority tasks."""
    info = get_host_and_api_or_query_key(trigger.sender, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])
    result = phabapi.dophabsearch(info[0], info[1], info[2], limit=False)
    if result:
        for task in result:
            bot.say(task, trigger.sender)
    else:
        bot.say("No tasks have high priority that I can see", trigger.sender)
