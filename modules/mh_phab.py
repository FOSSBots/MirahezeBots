"""This module contains commands related to Miraheze Phabricator."""

import json  # FIX THIS
import requests  # FIX THIS

from sopel import config
from sopel.module import commands, example, interval, rule
import sys

BOLD = '\x02'
HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []
config = config.Config('/data/project/zppixbot/.sopel/default.cfg')


def searchphab(bot, channel, task=1):
    data = {
        'api.token': config.phabricator.api_token,
        'constraints[ids][0]': task
    }
    response = requests.post(
        url='https://{0}/api/maniphest.search'.format(config.phabricator.host),
        data=data)
    response = response.json()
    go = 0
    try:
        result = response.get("result").get("data")[0]
        go = 1
    except AttributeError:
        bot.say("An error occurred while parsing the result.", channel)
        bot.say(response.text, "#ZppixBot-logs")
    except IndexError:
        bot.say("Sorry, but I couldn't find information for the task you searched.", channel)
    except:
        bot.say("An unknown error occured.", channel)
    if go == 1:
        params = {
            'api.token': config.phabricator.api_token,
            'constraints[phids][0]': result.get("fields").get("ownerPHID")
        }
        response2 = requests.post(
            url='https://{0}/api/user.search'.format(config.phabricator.host),
            data=params)
        try:
            response2 = response2.json()
        except json.decoder.JSONDecodeError as e:
            bot.say(response2.text, '#ZppixBot-Logs')
            bot.say(str(e), '#ZppixBot-Logs')
        params2 = {
            'api.token': config.phabricator.api_token,
            'constraints[phids][0]': result.get("fields").get("authorPHID")
        }
        response3 = requests.post(
            url='https://{0}/api/user.search'.format(config.phabricator.host),
            data=params2)
        response3 = response3.json()
        if result.get("fields").get("ownerPHID") is None:
            owner = None
        else:
            owner = response2.get("result").get("data")[0].get("fields").get("username")
        author = response3.get("result").get("data")[0].get("fields").get("username")
        priority = result.get("fields").get("priority").get("name")
        status = result.get("fields").get("status").get("name")
        output = 'https://phabricator.miraheze.org/T{0} - '.format(str(result["id"]))
        output = '{0}{2}{1}{2}, '.format(output, str(result.get('fields').get('name')), BOLD)
        output = output + 'authored by {1}{0}{1}, '.format(author, BOLD)
        output = output + 'assigned to {1}{0}{1}, '.format(owner, BOLD)
        output = output + 'Priority: {1}{0}{1}, '.format(priority, BOLD)
        output = output + 'Status: {1}{0}{1}'.format(status, BOLD)
        bot.say(output, channel)


def gethighpri(limit=True, channel='#miraheze', bot=None):
    data = {
        'api.token': config.phabricator.api_token,
        'queryKey': config.phabricator.querykey,  # mFzMevK.KRMZ for mhphab
    }
    response = requests.post(
        url='https://{0}/api/maniphest.search'.format(config.phabricator.host),
        data=data)
    response = response.json()
    result = response.get("result")
    try:
        data = result.get("data")
        go = 1
    except:
        bot.say("They are no high priority tasks that I can process, good job!", channel)
        go = 0
    if go == 1:
        x = 0
        while x < len(data):
            currdata = data[x]
            if x > 5 and limit:
                bot.say("They are more than 5 tasks. Please see {0} for the rest or use .highpri".format(
                    config.phabricator.host), channel)
                break
            else:
                searchphab(bot=bot, channel=channel, task=currdata.get("id"))
                x = x + 1


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    if trigger.group(2).startswith('T'):
        task_id = trigger.group(2).split('T')[1]
    else:
        task_id = trigger.group(2)
    searchphab(bot=bot, channel=trigger.sender, task=task_id)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = trigger.split('T')[1]
    searchphab(bot=bot, channel=trigger.sender, task=task_id)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send high priority tasks notifications."""
    gethighpri(bot=bot)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    gethighpri(limit=False, channel=trigger.sender, bot=bot)
