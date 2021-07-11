# type: ignore
"""phab.by - Phabricator Task Information Plugin."""

from MirahezeBots_jsonparser import jsonparser as jp
from sopel import bot, trigger, config
from sopel.config.types import (BooleanAttribute, ListAttribute, StaticSection,
                                ValidatedAttribute)
from sopel.plugin import commands, example, interval, require_admin, rule
from sopel.tools import SopelMemory, Identifier

from MirahezeBots.utils import phabapi


class PhabricatorSection(StaticSection):
    """Set up configuration for Sopel."""

    querykey = ListAttribute('querykey', str)
    api_token = ListAttribute('api_token', str)
    highpri_notify = BooleanAttribute('highpri_notify')
    highpri_channel = ValidatedAttribute('highpri_channel', str)
    datafile = ValidatedAttribute('datafile', str)


def setup(instance: bot) -> None:
    """Create the config section & memory."""
    instance.config.define_section('phabricator', PhabricatorSection)
    instance.memory['phab'] = SopelMemory()
    instance.memory['phab']['jdcache'] = jp.createdict(instance.settings.phabricator.datafile)


def configure(configuration: config) -> None:
    """Set up the configuration options."""
    configuration.define_section('phabricator', PhabricatorSection, validate=False)
    configuration.phabricator.configure_setting(
        'api_token',
        'Please enter a Phabricator API token.',
    )
    configuration.phabricator.configure_setting(
        'highpri_notify',
        'Would you like to enable automatic notification of high priority tasks? (true/false)',
    )
    configuration.phabricator.configure_setting(
        'highpri_channel',
        'If you enabled high priority notifications, what channel would you like them sent to? '
        '(notifications will be sent once every week.',
    )
    configuration.phabricator.configure_setting(
        'datafile',
        'File to read from to get channel specific data from',
    )
    configuration.phabricator.configure_setting(
        'querykey',
        'Please enter a Phabricator query key.',
    )


def get_host_and_api_or_query_key(channel: Identifier, cache: dict, keys: list) -> list:
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
    return [host, apikey, querykey]


@commands('task')
@example('.task 1')
def phabtask(instance: bot, message: trigger) -> None:
    """Get information on a phabricator task."""
    try:
        if message.group(2).startswith('T'):
            task_id = message.group(2).split('T')[1]
        else:
            task_id = message.group(2)
        info = get_host_and_api_or_query_key(
            message.sender,
            instance.memory['phab']['jdcache'],
            [
                instance.settings.phabricator.api_token,
                instance.settings.phabricator.querykey,
            ],
        )
        instance.reply(
            phabapi.gettaskinfo(
                info[0],
                info[1],
                task=task_id,
                session=instance.memory['shared']['session']),
            )
    except AttributeError:
        instance.say('Syntax: .task (task ID with or without T)', message.sender)


@rule('T[1-9][0-9]*')
def phabtask2(instance: bot, message: trigger) -> None:
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = str(message.match.group(0))[1:]
    info = get_host_and_api_or_query_key(
        message.sender,
        instance.memory['phab']['jdcache'],
        [
            instance.settings.phabricator.api_token,
            instance.settings.phabricator.querykey,
        ],
        )
    instance.reply(
        phabapi.gettaskinfo(
            info[0],
            info[1],
            task=task_id,
            session=instance.memory['shared']['session'],
        ),
    )


@interval(604800)  # every week
def high_priority_tasks_notification(instance: bot, message: trigger) -> None:  # noqa: U100
    """Send regular update on high priority tasks."""
    if instance.settings.phabricator.highpri_notify is True:
        info = get_host_and_api_or_query_key(
            instance.settings.phabricator.highpri_channel,
            instance.memory['phab']['jdcache'],
            [
                instance.settings.phabricator.api_token,
                instance.settings.phabricator.querykey,
            ],
        )
        result = phabapi.dophabsearch(
            info[0],
            info[1],
            info[2],
            session=instance.memory['shared']['session'],
            )
        if result:
            instance.say('Your weekly high priority task update:', instance.settings.phabricator.highpri_channel)
            for task in result:
                instance.say(task, instance.settings.phabricator.highpri_channel)
        else:
            instance.say(
                'High priority task update: Tasks exceeded limit or could not be found. Use ".highpri"',
                instance.settings.phabricator.highpri_channel,
            )


@commands('highpri')
@example('.highpri')
def forcehighpri(instance: bot, message: trigger) -> None:
    """Send full list of high priority tasks."""
    info = get_host_and_api_or_query_key(
        message.sender,
        instance.memory['phab']['jdcache'],
        [
            instance.settings.phabricator.api_token,
            instance.settings.phabricator.querykey,
        ],
    )
    result = phabapi.dophabsearch(
        info[0],
        info[1],
        info[2],
        limit=False,
        session=instance.memory['shared']['session']
        )
    if result:
        for task in result:
            instance.reply(task)
    else:
        instance.reply('No tasks have high priority that I can see')


@require_admin(message='Only admins may purge cache.')
@commands('resetphabcache')
def reset_phab_cache(instance: bot, message: trigger) -> None:  # noqa: U100
    """Reset the cache of the channel management data file."""
    instance.reply('Refreshing Cache...')
    instance.memory['phab']['jdcache'] = jp.createdict(instance.settings.phabricator.datafile)
    instance.reply('Cache refreshed')


@require_admin(message='Only admins may check cache')
@commands('checkphabcache')
def check_phab_cache(instance: bot, message: trigger) -> None:  # noqa: U100
    """Validate the cache matches the copy on disk."""
    result = jp.validatecache(instance.settings.phabricator.datafile, instance.memory['phab']['jdcache'])
    if result:
        instance.reply('Cache is correct.')
    else:
        instance.reply('Cache does not match on-disk copy')
