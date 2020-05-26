"""This module contains commands related to Miraheze Phabricator."""

import json  # FIX THIS
import requests  # FIX THIS

from sopel import config
from sopel.module import commands, example, interval, rule


HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []
config = config.Config('/data/project/zppixbot-test/.sopel/default.cfg')


def searchphab(bot, trigger):
    data = {
        'api.token': config.phabricator.api_token,
        'constraints[ids][0]': trigger.group(2)
    }
    response = requests.post(
        url='https://{0}/api/maniphest.search'.format(config.phabricator.host),
        data=data)
    response = response.json()
    result = response.get("result").get("data")[0]
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
    owner = response2.get("result").get("data")[0].get("fields").get("username")
    author = response3.get("result").get("data")[0].get("fields").get("username")
    output = 'https://phabricator.miraheze.org/T{0} " - '.format(str(result["id"])
    output = '{0}{1}, authored by {2}, assigned to {3}'.format(output, str(result.get("fields").get("name")), author, str(owner))
    bot.say(output, trigger.sender)


def gethighpri(limit=True, channel='#miraheze', bot=None):
    data = {
        'api.token': config.phabricator.api_token,
        'queryKey': config.phabricator.querykey,  # mFzMevK.KRMZ for mhphab
    }
    response = requests.post(
        url='https://{0}/api/mainphest.search'.format(config.phabricator.host),
        data=data)
    response = response.json()
    result = response.get("result")
    try:
        data = result.get("data")
        go = 1
    except TypeError:
        bot.say("They are no high priority tasks that I can view, good job!", channel)
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
                params = {
                    'api.token': config.phabricator.api_token,
                    'constraints[phids][0]': currdata.get("fields").get("ownerPHID"),
                }
                response2 = requests.post(
                    url='https://{0}/api/user.search'.format(
                        config.phabricator.host),
                    data=params)
                response2 = response2.json()
                params2 = {
                    'api.token': config.phabricator.api_token,
                    'constraints[phids][0]': currdata.get("fields").get("authorPHID"),
                }
                response3 = requests.post(
                    url='https://{0}/api/user.search'.format(
                        config.phabricator.host),
                    data=params2)
                response3 = response3.json()
                owner = response2["result"]["data"][0]["fields"]["username"]
                author = response3["result"]["data"][0]["fields"]["username"]
                output = 'https://phabricator.miraheze.org/T{0} - {1}, authored by {2}, assigned to {3})'.format(
                    str(currdata["id"]), str(currdata.get("fields").get("name")), author, str(owner))
                bot.say(output, channel)
                x = x + 1


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    searchphab(bot, trigger)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    bot.say("If you're expecting info on phab task to show up, nag RhinosF1 to fix this and use .task", trigger.sender)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send high priority tasks notifications."""
    gethighpri(bot=bot)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    gethighpri(limit=False, channel=trigger.sender, bot=bot)
