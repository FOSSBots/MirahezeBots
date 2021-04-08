"""phab.by - Phabricator Task Information Plugin."""

from MirahezeBots.utils import phabapi

from MirahezeBots_jsonparser import jsonparser as jp

from sopel.config.types import ListAttribute, StaticSection, ValidatedAttribute
from sopel.module import commands, example, interval, require_admin, rule
from sopel.tools import SopelMemory


class PhabricatorSection(StaticSection):
    """Set up configuration for Sopel."""

    querykey = ListAttribute('querykey', str)
    api_token = ListAttribute('api_token', str)
    highpri_notify = ValidatedAttribute('highpri_notify', bool)
    highpri_channel = ValidatedAttribute('highpri_channel', str)
    datafile = ValidatedAttribute('datafile', str)


def setup(bot):
    """Create the config section & memory."""
    bot.config.define_section('phabricator', PhabricatorSection)
    bot.memory['phab'] = SopelMemory()
    bot.memory['phab']['jdcache'] = jp.createdict(bot.settings.phabricator.datafile)


def configure(config):
    """Set up the configuration options."""
    config.define_section('phabricator', PhabricatorSection, validate=False)
    config.phabricator.configure_setting(
        'api_token',
        'Please enter a Phabricator API token.',
        )
    config.phabricator.configure_setting(
        'highpri_notify',
        'Would you like to enable automatic notification of high priority tasks? (true/false)',
        )
    config.phabricator.configure_setting(
        'highpri_channel',
        'If you enabled high priority notifications, what channel would you like them sent to? '
        '(notifications will be sent once every week.',
        )
    config.phabricator.configure_setting(
        'datafile',
        'File to read from to get channel specific data from',
        )
    config.phabricator.configure_setting(
        'querykey',
        'Please enter a Phabricator query key.',
        )


def get_host_and_api_or_query_key(channel, cache, keys):
    """Get hostname,apikey and querykey for instance."""
    if channel in cache:
        host = cache[str(channel)]['host']
        arraypos = int(cache[str(host)]['arraypos'])
        apikey = keys[0][int(arraypos)]
        querykey = keys[1][int(arraypos)]
    else:
        host = cache['default']['host']
        arraypos = int(cache[str(host)]['arraypos'])
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
        info = get_host_and_api_or_query_key(
            trigger.sender,
            bot.memory['phab']['jdcache'],
            [
                bot.settings.phabricator.api_token,
                bot.settings.phabricator.querykey,
            ],
            )
        bot.reply(phabapi.gettaskinfo(info[0], info[1], task=task_id, session=bot.memory['shared']['session']))
    except AttributeError:
        bot.say('Syntax: .task (task ID with or without T)', trigger.sender)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = (trigger.match.group(0)).split('T')[1]
    info = get_host_and_api_or_query_key(
        trigger.sender,
        bot.memory['phab']['jdcache'],
        [
            bot.settings.phabricator.api_token,
            bot.settings.phabricator.querykey,
        ],
        )
    bot.reply(phabapi.gettaskinfo(info[0], info[1], task=task_id, session=bot.memory['shared']['session']))


@interval(604800)  # every week
def high_priority_tasks_notification(bot):
    """Send regular update on high priority tasks."""
    if bot.settings.phabricator.highpri_notify is True:
        info = get_host_and_api_or_query_key(
            bot.settings.phabricator.highpri_channel,
            bot.memory['phab']['jdcache'],
            [
                bot.settings.phabricator.api_token,
                bot.settings.phabricator.querykey,
            ],
            )
        result = phabapi.dophabsearch(info[0], info[1], info[2], session=bot.memory['shared']['session'])
        if result:
            bot.say('Your weekly high priority task update:', bot.settings.phabricator.highpri_channel)
            for task in result:
                bot.say(task, bot.settings.phabricator.highpri_channel)
        else:
            bot.say(
                'High priority task update: Tasks exceeded limit or could not be found. Use ".highpri"',
                bot.settings.phabricator.highpri_channel,
                )


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    """Send full list of high priority tasks."""
    info = get_host_and_api_or_query_key(
        trigger.sender,
        bot.memory['phab']['jdcache'],
        [
            bot.settings.phabricator.api_token,
            bot.settings.phabricator.querykey,
        ],
        )
    result = phabapi.dophabsearch(info[0], info[1], info[2], limit=False, session=bot.memory['shared']['session'])
    if result:
        for task in result:
            bot.say(task, trigger.sender)
    else:
        bot.say('No tasks have high priority that I can see', trigger.sender)


@require_admin(message='Only admins may purge cache.')
@commands('resetphabcache')
def reset_phab_cache(bot, trigger):  # noqa: U100
    """Reset the cache of the channel management data file."""
    bot.reply('Refreshing Cache...')
    bot.memory['phab']['jdcache'] = jp.createdict(bot.settings.phabricator.datafile)
    bot.reply('Cache refreshed')


@require_admin(message='Only admins may check cache')
@commands('checkphabcache')
def check_phab_cache(bot, trigger):  # noqa: U100
    """Validate the cache matches the copy on disk."""
    result = jp.validatecache(bot.settings.phabricator.datafile, bot.memory['phab']['jdcache'])
    if result:
        bot.reply('Cache is correct.')
    else:
        bot.reply('Cache does not match on-disk copy')
