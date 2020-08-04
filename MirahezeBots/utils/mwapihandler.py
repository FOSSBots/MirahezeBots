import requests
import re
import time
import random
import json


def login(url, session, username='Example', password='password'):
  # Step 1: GET request to fetch login token

    PARAMS_0 = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json',
    }

    try:
        R = session.get(url=url, params=PARAMS_0)
        DATA = R.json()
    except BaseException:
        bot.reply("Catostrophic Error! Unable to connect to the wiki.")
        return

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

    PARAMS_1 = {
        'action': 'login',
        'lgname': username,
        'lgpassword': password,
        'lgtoken': LOGIN_TOKEN,
        'format': 'json',
    }
    try:
        R = session.post(url, data=PARAMS_1)
    except:
        bot.reply("Catastrophic Error! Unable to connect to the wiki.")
        return


def gettoken(url, session, type='csrftoken'):
  # Step 3: GET request to fetch CSRF token

    PARAMS_2 = {'action': 'query', 'meta': 'tokens', 'format': 'json'}

    try:
        R = session.get(url=url, params=PARAMS_2)
        DATA = R.json()
    except BaseException:
        bot.reply("Catastrophic Error! Unable to connect to the wiki.")
        return

    TOKEN = DATA['query']['tokens'][type]
    return TOKEN


def main(performer, target, action, reason, url, username, password):
    session = requests.Session()
    login(url, session, username, password)
    CSRF_TOKEN = gettoken(url, session, type='crsftoken')

# Step 4: POST request to perform action -- TO MIGRATE

    if action == 'edit':
        PARAMS_3 = {
            'action': 'edit',
            'title': target,
            'summary': reason + ' (' + performer + ')',
            'appendtext': '\n* ' + performer + ': ' + reason,
            'token': CSRF_TOKEN,
            'bot': 'true',
            'format': 'json',
        }

        try:
            R = session.post(URL, data=PARAMS_3)
            DATA = R.json()
            if DATA.get("error").get("info") is not None:
              return None
                # bot.say(DATA.get("error").get("info"))
            else:
              return None
                #bot.say("Logged message")
        except:
            bot.reply("An unexpected error occurred. Do I have edit rights on that wiki?")
    elif action == 'block':
        PARAMS_3 = {
            'action': 'block',
            'user': target,
            'expiry': 'infinite',
            'reason': 'Blocked by ' + performer + ' for ' + reason,
            'bot': 'false',
            'token': CSRF_TOKEN,
            'format': 'json',
        }

        try:
            R = session.post(url, data=PARAMS_3)
            DATA = R.json()
            if DATA.get("error").get("info") is not None:
                return None
                # bot.say(DATA.get("error").get("info"))
            else:
                return None
                #bot.reply("Block request sent. You may want to check the block log to be sure that it worked.")
        except:
            return None
            #bot.reply("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")
    elif action == 'unblock':
        PARAMS_3 = {
            'action': 'unblock',
            'user': target,
            'reason': 'Requested by ' + performer + ' Reason: ' + reason,
            'token': CSRF_TOKEN,
            'format': 'json',
        }

        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            if DATA.get("error") is not None:
                bot.say(DATA.get("error").get("info"))
            else:
                return None
            #bot.reply("Unblock request sent. You may want to check the block log to be sure that it worked.")
        except:
            return None
            #bot.reply("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")

    elif action == 'delete':
        PARAMS_3 = {
            'action': 'delete',
            'title': target,
            'reason': 'Requested by ' + performer + ' Reason: ' + reason,
            'token': CSRF_TOKEN,
            'format': 'json',
        }

        try:
            R = session.post(url, data=PARAMS_3)
            DATA = R.json()
            if DATA.get("error") is not None:
                return None
                # bot.say(DATA.get("error").get("info"))
            else:
                return None
                #bot.reply("Delete request sent. You may want to check the delete log to be sure that it worked.")
        except:
            return None
            #bot.reply("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")