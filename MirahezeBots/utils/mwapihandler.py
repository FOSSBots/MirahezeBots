""" The functions in this file are not suitable for non-internal use. They are subject to change without notice and are not yet released. """
import requests
import re
import time
import random


def login(url, session, username='Example', password='password'):
    PARAMS_0 = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json',
    }
    try:
        request = session.get(url=url, params=PARAMS_0)
        DATA = request.json()
    except:
        return ["Error", "Unable to conect to wiki"]

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    PARAMS_1 = {
        'action': 'login',
        'lgname': username,
        'lgpassword': password,
        'lgtoken': LOGIN_TOKEN,
        'format': 'json',
    }
    try:
        request = session.post(url, data=PARAMS_1)
    except:
        return ["Error", "Unable to conect to wiki"]


def gettoken(url, session, type='csrftoken'):
    PARAMS_2 = {'action': 'query', 'meta': 'tokens', 'format': 'json'}

    try:
        request = session.get(url=url, params=PARAMS_2)
        DATA = request.json()
    except:
        return ["Error", "Unable to conect to wiki"]

    TOKEN = DATA['query']['tokens'][type]
    return TOKEN


def makeaction(url, session, action, TOKEN, target, performer, reason, content=''):
    if action == 'edit':
        PARAMS = {
            'action': 'edit',
            'title': target,
            'summary': reason + ' (' + performer + ')',
            'appendtext': '\n* ' + performer + ': ' + reason,
            'token': TOKEN,
            'bot': 'true',
            'format': 'json',
        }
    elif action == "create":
        PARAMS = {
            'action': 'edit',
            'title': target,
            'summary': reason,
            'text': content,
            'token': TOKEN,
            'bot': 'true',
            'format': 'json',
            'contentmodel': 'wikitext',
            'recreate': True,
            'watchlist': 'nochange',
            'redirect': False,
        }

    elif action == 'block':
        PARAMS = {
            'action': 'block',
            'user': target,
            'expiry': 'infinite',
            'reason': 'Blocked by ' + performer + ' for ' + reason,
            'bot': 'false',
            'token': TOKEN,
            'format': 'json',
        }

    elif action == 'unblock':
        PARAMS = {
            'action': 'unblock',
            'user': target,
            'reason': 'Requested by ' + performer + ' Reason: ' + reason,
            'token': TOKEN,
            'format': 'json',
        }

    elif action == 'delete':
        PARAMS = {
            'action': 'delete',
            'title': target,
            'reason': 'Requested by ' + performer + ' Reason: ' + reason,
            'token': TOKEN,
            'format': 'json',
        }

    try:
        request = session.post(url, data=PARAMS)
        DATA = request.json()
        if DATA.get("error") is not None:
            return ["MWError", (DATA.get("error").get("info"))]
        else:
            return ["Success", ("{} request sent. You may want to check the {} log to be sure that it worked.").format(action, action)]
    except:
        return ["Fatal", ("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have {} rights on that wiki?").format(action)]


def main(performer, target, action, reason, url, username, password):
    session = requests.Session()
    lg = login(url, session, username, password)
    if lg[0] == "Error":
        return lg[1]
    else:
        TOKEN = gettoken(url, session, type='crsftoken')
        if TOKEN[0] == "Error":
            return TOKEN[1]
        else:
            act = makeaction(url, session, action, TOKEN, target, performer, reason)
            return act[1]
