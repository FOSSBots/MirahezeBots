"""phab.by - Phabricator Task Information Plugin"""

import json  # FIX THIS
import requests  # FIX THIS
from sopel.module import commands, example, interval, rule
from sopel.config.types import StaticSection, ValidatedAttribute
import sys


class PhabricatorSection(StaticSection):
    host = ValidatedAttribute('host', str)
    api_token = ValidatedAttribute('api_token', str)
    querykey = ValidatedAttribute('querykey', str)
    highpri_notify = ValidatedAttribute('highpri_notify', bool)
    highpri_channel = ValidatedAttribute('highpri_channel', str)


def setup(bot):
    bot.config.define_section('phabricator', PhabricatorSection)


def configure(config):
    config.define_section('phabricator', PhabricatorSection, validate=False)
    config.phabricator.configure_setting('host', 'What is the URL of your Phabricator installation?')
    config.phabricator.configure_setting('api_token', 'Please enter a Phabricator API token.')
    config.phabricator.configure_setting('querykey', 'Please enter a Phabricator query key.')
    config.phabricator.configure_setting('highpri_notify', 'Would you like to enable automatic notification of high priority tasks? (true/false)')
    config.phabricator.configure_setting('highpri_channel',
                                         'If you enabled high priority notifications, what channel would you like them sent to? (notifications will be sent once every week.')


BOLD = '\x02'
HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []


def searchphab(bot, channel, task=1):
    data = {
        'api.token': bot.settings.phabricator.api_token,
        'constraints[ids][0]': task
    }
    response = requests.post(
        url='https://{0}/api/maniphest.search'.format(bot.settings.phabricator.host),
        data=data)
    response = response.json()
    go = 0
    try:
        result = response.get("result").get("data")[0]
        go = 1
    except AttributeError:
        bot.say("An error occurred while parsing the result.", channel)
    except IndexError:
        bot.say("Sorry, but I couldn't find information for the task you searched.", channel)
    except:
        bot.say("An unknown error occured.", channel)
    if go == 1:
        params = {
            'api.token': bot.settings.phabricator.api_token,
            'constraints[phids][0]': result.get("fields").get("ownerPHID")
        }
        response2 = requests.post(
            url='https://{0}/api/user.search'.format(bot.settings.phabricator.host),
            data=params)
        try:
            response2 = response2.json()
        except json.decoder.JSONDecodeError as e:
            bot.say(response2.text, '#ZppixBot-Logs')
            bot.say(str(e), '#ZppixBot-Logs')
        params2 = {
            'api.token': bot.settings.phabricator.api_token,
            'constraints[phids][0]': result.get("fields").get("authorPHID")
        }
        response3 = requests.post(
            url='https://{0}/api/user.search'.format(bot.settings.phabricator.host),
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
        'api.token': bot.settings.phabricator.api_token,
        'queryKey': bot.settings.phabricator.querykey,  # mFzMevK.KRMZ for mhphab
    }
    response = requests.post(
        url='https://{0}/api/maniphest.search'.format(bot.settings.phabricator.host),
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
                    bot.settings.phabricator.host), channel)
                break
            else:
                searchphab(bot=bot, channel=channel, task=currdata.get("id"))
                x = x + 1


@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    try:
        if trigger.group(2).startswith('T'):
            task_id = trigger.group(2).split('T')[1]
        else:
            task_id = trigger.group(2)
        searchphab(bot=bot, channel=trigger.sender, task=task_id)
    except AttributeError:
        bot.say('Syntax: .task (task ID with or without T)', trigger.sender)


@rule('T[1-9][0-9]*')
def phabtask2(bot, trigger):
    """Get a Miraheze phabricator link to a the task number you provide."""
    task_id = (trigger.match.group(0)).split('T')[1]
    searchphab(bot=bot, channel=trigger.sender, task=task_id)


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    if bot.settings.phabricator.highpri_notify is True:
        """Send high priority tasks notifications."""
        gethighpri(channel=bot.settings.phabricator.highpri_channel, bot=bot)


@commands('highpri')
@example('.highpri')
def forcehighpri(bot, trigger):
    gethighpri(limit=False, channel=trigger.sender, bot=bot)
