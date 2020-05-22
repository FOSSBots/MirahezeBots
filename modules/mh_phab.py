"""This module contains commands related to Miraheze Phabricator."""

from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division
)

import os
import re
import sys
from time import time, sleep

from sopel.module import commands, example, interval, rule
# sopel modules import problem workaround
sys.path.insert(0, os.path.abspath(__file__ + "/.."))
from utils.phabricator import PhabricatorClient

HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []


def setup(bot):
    """Setup phabricator client."""
    global priotasks_notify
    if hasattr(bot.config, 'phabricator'):
        bot.phabricator = PhabricatorClient(
            bot.config.phabricator.host,
            bot.config.phabricator.api_token
        )

        if (hasattr(bot.config.phabricator, 'priotasks_notify') and bot.config.phabricator.priotasks_notify is not None):
            priotasks_notify = list(map(
                lambda f: f.strip(),
                bot.config.phabricator.priotasks_notify.split(',')
            ))


def mass_message(bot, targets, message):
    """Send the same message to multiple targets."""
    for target in targets:
        bot.say(message, target)
        sleep(MESSAGES_INTERVAL)


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


@commands('priotasks')
@example('.priotasks 2')
def high_priority_tasks_no_updates(bot, trigger):
    """Command to find high priority tasks whithout updates for a while."""
    if trigger.nick not in bot.config.core.admins:
        bot.reply('Only bot admins can search Phabricator tasks.')
        return

    tasks = bot.phabricator.find_tasks(
        priorities=[PhabricatorClient.PRIORITY_HIGH],
        statuses=[PhabricatorClient.STATUS_OPEN]
    )

    if len(tasks) == 0:
        bot.reply('There are no high priority open tasks. Nice job!')
        return

    page_number = 1
    if trigger.group(3):
        page_number = int(re.sub('[^0-9]', '', trigger.group(3)))
    if page_number <= 0:
        bot.reply('Invalid page number')
        return

    page_offset = (page_number - 1) * HIGHPRIO_NOTIF_TASKS_PER_PAGE
    tasks_waiting = 0
    page_overflow_tasks = 0

    for task in tasks:
        time_diff = int(round((time() - task.dateModified) / (24 * 60 * 60)))
        if time_diff < 3:
            continue
        if page_offset > 0:
            page_offset -= 1
            continue
        if tasks_waiting >= HIGHPRIO_NOTIF_TASKS_PER_PAGE:
            page_overflow_tasks += 1
            continue

        message = 'No updates for {} - {} - {} - authored by {}'.format(
            str(time_diff) + ' days',
            task.link,
            task.title,
            task.author.username
        )
        if task.owner is not None:
            message += ', assigned to {}'.format(task.owner.username)
        else:
            message += ', assigned to None'
        bot.say(message)
        sleep(MESSAGES_INTERVAL)

        tasks_waiting += 1

    if tasks_waiting == 0:
        if page_number == 0:
            bot.reply('No tasks with last update time > 3 days. Good job!')
        else:
            bot.reply('No tasks on this page')
    elif page_overflow_tasks != 0:
        bot.say('and {} more (see page {}...)'.format(
            page_overflow_tasks,
            page_number + 1
        ))


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send high priority tasks notifications."""
    tasks = bot.phabricator.find_tasks(
        priorities=[PhabricatorClient.PRIORITY_HIGH],
        statuses=[PhabricatorClient.STATUS_OPEN]
    )

    if len(tasks) == 0:
        mass_message(bot, priotasks_notify, 'Hi! Just contacting you to tell '
                     'that here are no high priority open tasks. Nice job!')
        return

    tasks_waiting = 0
    page_overflow_tasks = 0

    for task in tasks:
        time_diff = int(round((time() - task.dateModified) / (24 * 60 * 60)))
        if time_diff < 3:
            continue
        if tasks_waiting >= HIGHPRIO_NOTIF_TASKS_PER_PAGE:
            page_overflow_tasks += 1
            continue

        if tasks_waiting == 0:
            mass_message(bot, priotasks_notify, 'Hi! Here is the list of '
                         'currently open high priority tasks on Phabricator')

        message = 'No updates for {} - {} - {} - authored by {}'.format(
            str(time_diff) + ' days',
            task.link,
            task.title,
            task.author.username
        )
        if task.owner is not None:
            message += ', assigned to {}'.format(task.owner.username)
        else:
            message += ', assigned to None'

        mass_message(bot, priotasks_notify, message)

        tasks_waiting += 1

    if tasks_waiting == 0:
        mass_message(bot, priotasks_notify, 'Hi! Just contacting you to tell '
                     'that here are no high priority open tasks with last '
                     'update time > 3 days. Nice job!')
    elif page_overflow_tasks != 0:
        mass_message(bot, priotasks_notify,
                     'and {} more (see next pages...)'.format(
                         page_overflow_tasks
                     ))


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = int(re.sub("[^0-9]", "", trigger))

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
