"""This module contains commands related to Miraheze Phabricator."""

from sopel.module import commands, example, interval, rule, config
import requests
HIGHPRIO_NOTIF_TASKS_PER_PAGE = 5
HIGHPRIO_TASKS_NOTIFICATION_INTERVAL = 7 * 24 * 60 * 60  # every week
MESSAGES_INTERVAL = 2  # seconds (to avoid excess flood)
startup_tasks_notifications = False
priotasks_notify = []

def mass_message(bot, targets, message):
    """Send the same message to multiple targets."""
    for target in targets:
        bot.say(message, target)
        sleep(MESSAGES_INTERVAL)

def searchphab():
    
def gethighpri():
    data = {
        'api.token': config.phabricator.api_token
        'queryKey': config.phabricator.querykey #mFzMevK.KRMZ for mhphab
    }
    response = requests.post(url='https://'+config.phabricator.host+'/api/mainphest.search', data=data)
    response = response.json()
    result = response["result"]
    data = result["data"]
    
    
@commands('task')
@example('.task 1')
def phabtask(bot, trigger):
    searchphab()

@rule('T[1-9][0-9]*')	
def phabtask2(bot, trigger):	
    """Get a Miraheze phabricator link to a the task number you provide."""
    searchphab()


@interval(HIGHPRIO_TASKS_NOTIFICATION_INTERVAL)
def high_priority_tasks_notification(bot):
    """Send high priority tasks notifications."""
    gethighpri()
