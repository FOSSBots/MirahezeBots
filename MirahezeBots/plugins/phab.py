"""phab.by - Phabricator Task Information Plugin."""

from MirahezeBots.utils import phabapi

from MirahezeBots_jsonparser import jsonparser as jp

from sopel.config.types import ListAttribute, StaticSection, ValidatedAttribute
from sopel.module import commands, example, interval, require_admin, rule
from sopel.tools import SopelMemory


class PhabricatorSection(StaticSection):
    """Set up configuration for Sopel."""

    host = ValidatedAttribute('host', str)
    api_token = ListAttribute('api_token', str)
    querykey = ListAttribute('querykey', str)
    highpri_notify = ValidatedAttribute('highpri_notify', bool)
    highpri_channel = ValidatedAttribute('highpri_channel', str)
    datafile = ValidatedAttribute('datafile', str)


def setup(bot):
    """Create the config section & memory."""
    bot.config.define_section('phabricator', PhabricatorSection)
    bot.memory["phab"] = SopelMemory()
    bot.memory["phab"]["jdcache"] = jp.createdict(bot.settings.phabricator.datafile)


def configure(config):
    """Set up the configuration options."""
    config.define_section('phabricator', PhabricatorSection, validate=False)
    config.phabricator.configure_setting('host', 'What is the URL of your Phabricator installation?')
    config.phabricator.configure_setting('api_token', 'Please enter a Phabricator API token.')
    config.phabricator.configure_setting('querykey', 'Please enter a Phabricator query key.')
    config.phabricator.configure_setting('highpri_notify', 'Would you like to enable automatic notification of high priority tasks? (true/false)')
    config.phabricator.configure_setting('highpri_channel',
                                         'If you enabled high priority notifications, what channel would you like them sent to? (notifications will be sent once every week.')
    config.phabricator.configure_setting('datafile', 'File to read from to get channel specific data from')


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
        phabapi.gettaskinfo(info[0], info[1], task=task_id)
    except AttributeError:
        bot.say('Syntax: .task (task ID with or without T)', trigger.sender)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = (trigger.match.group(0)).split('T')[1]
    info = get_host_and_api_or_query_key(trigger.sender, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])
    phabapi.gettaskinfo(info[0], info[1], task=task_id)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send regular update on high priority tasks."""
    if bot.settings.phabricator.highpri_notify is True:
        """Send high priority tasks notifications."""
        info = get_host_and_api_or_query_key(bot.settings.phabricator.highpri_channel, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])
        phabapi.dophabsearch(info[0], info[1], info[2])


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    """Send full list of high priority tasks."""
    info = get_host_and_api_or_query_key(trigger.sender, bot.memory["phab"]["jdcache"], [bot.settings.phabricator.api_token, bot.settings.phabricator.querykey])
    phabapi.dophabsearch(info[0], info[1], info[2], limit=False)


@require_admin(message="Only admins may purge cache.")
@commands('resetphabcache')
def reset_phab_cache(bot, trigger):  # noqa: U100
    """Reset the cache of the channel management data file."""
    bot.reply("Refreshing Cache...")
    bot.memory["phab"]["jdcache"] = jp.createdict(bot.settings.phabricator.datafile)
    bot.reply("Cache refreshed")


@require_admin(message="Only admins may check cache")
@commands('checkphabcache')
def check_phab_cache(bot, trigger):  # noqa: U100
    """Validate the cache matches the copy on disk."""
    result = jp.validatecache(bot.settings.phabricator.datafile, bot.memory["phab"]["jdcache"])
    if result:
        bot.reply("Cache is correct.")
    else:
        bot.reply("Cache does not match on-disk copy")
