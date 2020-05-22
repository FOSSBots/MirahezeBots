"""This module contains commands related to Miraheze Phabricator."""

import requests  # FIX THIS
from phabricator import Phabricator
import json  # FIX THIS
from sopel import config
from sopel.module import commands, example, interval, rule
HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []
config = config.Config('$HOME/.sopel/default.cfg')


def searchphab(bot, trigger):
    data = {
        'api.token': config.phabricator.api_token,
        'constraints[ids][0]': trigger.group(2)
    }
    response = requests.post(
        url='https://' + config.phabricator.host + '/api/maniphest.search',
        data=data)
    response = response.json()
    result = response["result"]["data"][0]
    params = {
        'api.token': config.phabricator.api_token,
        'constraints[phids][0]': result["fields"]["ownerPHID"]
    }
    response2 = requests.post(
        url='https://' + config.phabricator.host + '/user.search',
        data=params)
    response2 = response2.json()
    params2 = {
        'api.token': config.phabricator.api_token,
        'constraints[phids][0]': result["fields"]["authorPHID"]
    }
    response3 = requests.post(
        url='https://' + config.phabricator.host + '/api/user.search',
        data=params2)
    response3 = response3.json()
    owner = response2["result"]["data"][0]["fields"]["username"]
    author = response3["result"]["data"][0]["fields"]["username"]
    output = "https://phabricator.miraheze.org/T" + str(result["id"]) + " - " + str(
        result["fields"]["name"] + ", authored by " + author + ", assigned to " + str(owner))
    bot.say(output, trigger.sender)


def gethighpri(limit=True, channel='#miraheze', bot=None):
    data = {
        'api.token': config.phabricator.api_token,
        'queryKey': config.phabricator.querykey,  # mFzMevK.KRMZ for mhphab
    }
    response = requests.post(
        url='https://' + config.phabricator.host + '/api/mainphest.search',
        data=data)
    response = response.json()
    result = response["result"]
    data = result["data"]
    x = 0
    while x < len(data):
        currdata = data[x]
        if x > 5 and limit is True:
            bot.say("They are more than 5 tasks. Please see " + config.phabricator.host + " for the rest or use .highpri", channel)
            break
        else:
            params = {
                'api.token': config.phabricator.api_token,
                'constraints[phids][0]': currdata["fields"]["ownerPHID"],
            }
            response2 = requests.post(
                url='https://' + config.phabricator.host + '/api/user.search',
                data=params)
            response2 = response2.json()
            params2 = {
                'api.token': config.phabricator.api_token,
                'constraints[phids][0]': currdata["fields"]["authorPHID"],
            }
            response3 = requests.post(
                url='https://' + config.phabricator.host + '/api/user.search',
                data=params2)
            response3 = response3.json()
            owner = response2["result"]["data"][0]["fields"]["username"]
            author = response3["result"]["data"][0]["fields"]["username"]
            output = "https://phabricator.miraheze.org/T" + str(currdata["id"]) + " - " + str(currdata["fields"]["name"] + ", authored by " + author + ", assigned to " + str(owner))
            bot.say(output, channel)
            x = x + 1


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    searchphab(bot, trigger)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    searchphab(bot, trigger)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send high priority tasks notifications."""
    gethighpri(bot=bot)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    gethighpri(limit=False, channel=trigger.sender, bot=bot)
