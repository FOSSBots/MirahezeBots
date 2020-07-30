"""wikimgnt.py - interact with MediaWiki"""

import requests
import re
import time
import random

from sopel.module import rule, commands, example
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute


class WikimgntSection(StaticSection):
    log_wiki_url = ValidatedAttribute('log_wiki_url', str)
    log_page = ValidatedAttribute('log_page', str)
    wiki_acl = ListAttribute('wiki_acl')
    wiki_farm = ValidatedAttribute('wiki_farm', bool)
    wiki_domain = ValidatedAttribute('wiki_domain', str)
    wiki_username = ValidatedAttribute('wiki_username', str)
    wiki_password = ValidatedAttribute('wiki_password', str)


def setup(bot):
    bot.config.define_section('wikimgnt', WikimgntSection)


def configure(config):
    config.define_section('wikimgnt', WikimgntSection, validate=False)
    config.wikimgnt.configure_setting('log_wiki_url', 'What is the URL of the wiki that you would like .log messages to go to? Please specify the URL to that wikis api.php.')
    config.wikimgnt.configure_setting('log_page', 'What page on that wiki would like .log messages to go to? Instead of a space, type a _ please.')
    config.wikimgnt.configure_setting('wiki_acl', 'Please enter NickServ accounts that are allowed to use the commands in this module. (No spaces)')
    config.wikimgnt.configure_setting('wiki_farm', 'Are you using this for a wiki farm? (true/false)')
    config.wikimgnt.configure_setting('wiki_domain', 'If you said true to the previous question then What the domain name of your wiki farm? Please specify  the URL to api.php without a subdomain. If you said false, please specify the URL of your wikis api.php.')
    config.wikimgnt.configure_setting('wiki_username', 'What is the wikimgnt wiki username? (from Special:BotPasswords)')
    config.wikimgnt.configure_setting('wiki_password', 'What is the wikimgnt wiki password? (from Special:BotPasswords)')


def main(bot, trigger, performer, target, action, reason):
    S = requests.Session()

    URL = target

# Step 1: GET request to fetch login token

    PARAMS_0 = {
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json',
        }

    try:
        R = S.get(url=URL, params=PARAMS_0)
        DATA = R.json()
    except:
        bot.reply("Catostrophic Error! Unable to connect to the wiki.")
        return

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

# Step 2: POST request to log in. Use of main account for login is not
# supported. Obtain credentials via Special:BotPasswords
# (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword

    PARAMS_1 = {
        'action': 'login',
        'lgname': bot.settings.wikimgnt.wiki_username,
        'lgpassword': bot.settings.wikimgnt.wiki_password,
        'lgtoken': LOGIN_TOKEN,
        'format': 'json',
        }
    try:
        R = S.post(URL, data=PARAMS_1)
   except:
        bot.reply("Catastrophic Error! Unable to connect to the wiki.")
        return

# Step 3: GET request to fetch CSRF token

    PARAMS_2 = {'action': 'query', 'meta': 'tokens', 'format': 'json'}

    try:
        R = S.get(url=URL, params=PARAMS_2)
        DATA = R.json()
    except:
        bot.reply("Catastrophic Error! Unable to connect to the wiki.")
        return

    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']

# Step 4: POST request to perform action

    if action == 'edit':
        PARAMS_3 = {
            'action': 'edit',
            'title': bot.settings.wikimgnt.log_page,
            'summary': reason + ' (' + performer + ')',
            'appendtext': '\n* ' + performer + ': ' + reason,
            'token': CSRF_TOKEN,
            'bot': 'true',
            'format': 'json',
            }

        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            bot.say("Logged message at https://ops.miraheze.org/wiki/Global_IRC_Log")
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
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            bot.reply("Block request sent. You may want to check the block log to be sure that it worked.")
        except:
            bot.reply("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")
            return
    elif action == 'unblock':
        PARAMS_3 = {
            'action': 'unblock',
            'user': target,
            'reason': 'Requested by ' + performer + ' Reason: ' \
                + reason,
            'token': CSRF_TOKEN,
            'format': 'json',
            }

        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            bot.reply("Unblock request sent. You may want to check the block log to be sure that it worked.")
        except:
            bot.reply("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")

    elif action == 'delete':
        PARAMS_3 = {
            'action': 'delete',
            'title': target,
            'reason': 'Requested by ' + performer + ' Reason: ' \
                + reason,
            'token': CSRF_TOKEN,
            'format': 'json',
            }

        try:
            R = S.post(URL, data=PARAMS_3)
            DATA = R.json()
            bot.reply("Delete request sent. You may want to check the deletion log to be sure that it worked.")
        except:
            bot.reply("An unexpected error occurred. Did you type the wiki or user incorrectly? Do I have admin rights on that wiki?")


@commands('log')
@example('.log restarting sopel')
def logpage(bot, trigger):
    """Log given message to configured page"""
    if trigger.account in bot.settings.wikimgnt.wiki_acl:
        sender = trigger.nick
        url = bot.settings.wikimgnt.log_wiki_url
        if trigger.group(2) is None:
            bot.say("Syntax: .log message")
        else:
            message = trigger.group(2)
            main(bot, trigger, sender, 'edit', url, message)
    else:
        bot.reply("Sorry: you don't have permission to use this module")


@commands('delete')
@example('.delete Test_page vandalism')
@example('.delete test Test_page vandalism')
def deletepage(bot, trigger):
    """Delete the given page (depending on config, on the given wiki)"""
    if trigger.account in bot.settings.wikimgnt.wiki_acl:
        options = trigger.group(2).split(" ")
        sender = trigger.nick
        if bot.settings.wikimgnt.wiki_farm is True:
            if len(options) < 3:
                bot.say("Syntax: .delete wiki page reason")
            else:
                url = options[1] + '.' + bot.settings.wikimgnt.wiki_domain
                target = options[2]
                reason = options[3]
                main(bot, trigger, sender, delete, url, reason)
        else:
            if len(options) < 2:
                bot.say("Syntax: .delete page reason")
            else:
                url = bot.settings.wikimgnt.wiki_domain
                target = options[1]
                reason = options[2]
                main(bot, trigger, sender, delete, url, reason)
    else:
        bot.reply("Sorry: you don't have permission to use this module")


@commands('block')
@example('.block Zppix vandalism')
@example('.block test Zppix vandalism')
def blockuser(bot, trigger):
    """Block the given user indefinitely (depending on config, on the given wiki)"""
    if trigger.account in bot.settings.wikimgnt.wiki_acl:
        options = trigger.group(2).split(" ")
        sender = trigger.nick
        if bot.settings.wikimgnt.wiki_farm is True:
            if len(options) < 3:
                bot.say("Syntax: .block wiki user reason")
            else:
                url = options[1] + '.' + bot.settings.wikimgnt.wiki_domain
                target = options[2]
                reason = options[3]
                main(bot, trigger, sender, block, url, reason)
        else:
            if len(options) < 2:
                bot.say("Syntax: .block user reason")
            else:
                url = bot.settings.wikimgnt.wiki_domain
                target = options[1]
                reason = options[2]
                main(bot, trigger, sender, block, url, reason)
    else:
        bot.reply("Sorry: you don't have permission to use this module")


@commands('unblock')
@example('.unblock Zppix appeal')
@example('.unblock test Zppix per appeal')
def unblockuser(bot, trigger):
    """Unblock the given user (depending on config, on the given wiki)"""
    if trigger.account in bot.settings.wikimgnt.wiki_acl:
        options = trigger.group(2).split(" ")
        sender = trigger.nick
        if bot.settings.wikimgnt.wiki_farm is True:
            if len(options) < 3:
                bot.say("Syntax: .unblock wiki user reason")
            else:
                url = options[1] + '.' + bot.settings.wikimgnt.wiki_domain
                target = options[2]
                reason = options[3]
                main(bot, trigger, sender, unblock, url, reason)
        else:
            if len(options) < 2:
                bot.say("Syntax: .unblock user reason")
            else:
                url = bot.settings.wikimgnt.wiki_domain
                target = options[1]
                reason = options[2]
                main(bot, trigger, sender, unblock, url, reason)
    else:
        bot.reply("Sorry: you don't have permission to use this module")
