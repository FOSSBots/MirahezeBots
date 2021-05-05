"""MediaWiki API Handler."""
import requests


CONNECTERRMSG = 'Unable to conect to wiki'


def login(url, session, username, password):
    """Login to MediaWiki API using bot password system."""
    PARAMS_0 = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json',
    }
    try:
        request = session.get(url=url, params=PARAMS_0)
        DATA = request.json()
    except Exception:
        return ['Error', CONNECTERRMSG]

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    PARAMS_1 = {
        'action': 'login',
        'lgname': username,
        'lgpassword': password,
        'lgtoken': LOGIN_TOKEN,
        'format': 'json',
    }
    try:
        session.post(url, data=PARAMS_1)
    except Exception:
        return ['Error', CONNECTERRMSG]
    return ['Success', 'Logged in']


def gettoken(url, session, tokentype='csrftoken'):
    """Get a token from the meta::tokens api."""
    PARAMS_2 = {'action': 'query', 'meta': 'tokens', 'format': 'json'}

    try:
        request = session.get(url=url, params=PARAMS_2)
        DATA = request.json()
    except Exception:
        return ['Error', CONNECTERRMSG]

    return DATA['query']['tokens'][tokentype]


def makeaction(requestinfo, action, target, performer, reason, content=''):
    """Perform an action via the ACTIONS API."""
    if action == 'edit':
        PARAMS = {
            'action': 'edit',
            'title': target,
            'summary': reason + ' (' + performer + ')',
            'appendtext': '\n* ' + performer + ': ' + reason,
            'token': requestinfo[2],
            'bot': 'true',
            'format': 'json',
        }
    elif action == 'create':
        PARAMS = {
            'action': 'edit',
            'title': target,
            'summary': reason,
            'text': content,
            'token': requestinfo[2],
            'bot': 'true',
            'format': 'json',
            'contentmodel': 'wikitext',
            'recreate': True,
            'watchlist': 'nochange',
        }

    elif action == 'block':
        PARAMS = {
            'action': 'block',
            'user': target,
            'expiry': 'infinite',
            'reason': 'Blocked by ' + performer + ' for ' + reason,
            'bot': 'false',
            'token': requestinfo[2],
            'format': 'json',
        }

    elif action == 'unblock':
        PARAMS = {
            'action': 'unblock',
            'user': target,
            'reason': 'Requested by ' + performer + ' Reason: ' + reason,
            'token': requestinfo[2],
            'format': 'json',
        }

    elif action == 'delete':
        PARAMS = {
            'action': 'delete',
            'title': target,
            'reason': 'Requested by ' + performer + ' Reason: ' + reason,
            'token': requestinfo[2],
            'format': 'json',
        }

    try:
        request = requestinfo[1].post(requestinfo[0], data=PARAMS)
        DATA = request.json()
        if DATA.get('error') is not None:
            return ['MWError', (DATA.get('error').get('info'))]
        return ['Success', f'{action} request sent. You may want to check the {action} log to be sure that it worked.']
    except Exception:
        return [
            'Fatal',
            f'An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have {action} on that wiki?',
            ]  # noqa: JS102


def main(performer, target, action, reason, url, authinfo, content=False, session=requests.Session()):
    """Execute a full API Sequence."""
    lg = login(url, session, authinfo[0], authinfo[1])
    if lg[0] == 'Error':
        return lg[1]
    TOKEN = gettoken(url, session, tokentype='csrftoken')
    if TOKEN[0] == 'Error':
        return TOKEN[1]
    if content:
        return makeaction([url, session, TOKEN], action, target, performer, reason, content)[1]
    return makeaction([url, session, TOKEN], action, target, performer, reason)[1]
