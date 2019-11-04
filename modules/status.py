from __future__ import unicode_literals, absolute_import, print_function, division
import configparser
import json
import mwclient
from mwclient import errors
import requests
import re
import time
from sopel.module import rule, commands, example


pages = ''


def save_wrap(site, request, bot, trigger):
    pagename = 'User:' + request[0] + '/Status'
    bot.say(trigger.nick + ": Updating " + pagename + " to " + request[1] + "!", trigger.sender)
    page = site.Pages[pagename]
    save_edit(page, request[1], bot, trigger)


def save_edit(page, status, bot, trigger):
    time.sleep(5)
    edit_summary = "BOT: Setting Status to:" + status + " per " + trigger.hostmask
    times = 0
    while True:
        if times > 1:
            break
        try:
            page.save(status, summary=edit_summary, bot=True, minor=True)
            bot.say(trigger.nick + ": Updated!", trigger.sender)
        except errors.ProtectedPageError:
            print('Could not edit ' + page + ' due to protection')
            bot.say(trigger.nick + ": Error: Page Protected", trigger.sender)
            times += 1
        except errors.EditError:
            print("Error")
            bot.say(trigger.nick + ": An Error Occured :(", trigger.sender)
            times += 1
            time.sleep(5)  # sleep for 5 seconds before trying again
            continue
        except errors.UserBlocked:
            bot.say(trigger.nick + ": StatusBot is currently unavaiable for that wiki. Our team are working on it!", trigger.sender)
            bot.say("ERR: The bot is blocked on " + page, '#ZppixBot')
        except requests.exceptions.Timeout:
            bot.say(trigger.nick + ": We're experinecing delays connecting to that wiki. Try again in a few minutes. If this continues, let us know in #ZppixBot.", trigger.sender)
        except requests.exceptions.TooManyRedirects as e:
            bot.say(trigger.nick + ": We couldn't connect to that wiki. I've alerted a maintainer in #ZppixBot.", trigger.sender)
            bot.say("Redirect Error: " + e, '#ZppixBot-logs')
       except requests.exceptions.ConnectionError as e:
            bot.say(trigger.nick + ": We couldn't connect to that wiki. I've alerted a maintainer in #ZppixBot.", trigger.sender)
            bot.say("ConnectionError:" + e, '#ZppixBot-logs')
       except requests.exceptions.RequestException as e:
            bot.say(trigger.nick + ": A fatal error occured. I've alrted a maintainer in #ZppixBot.", trigger.sender)
            bot.say("Fatal Error: " + e, '#ZppixBot-logs') 
       break


def main(bot, trigger, options):
    cont = 0
    if len(options) == 2:
        wiki = options[0]
        status = options[1]
        host = trigger.host
        host = host.split('/')
        cont = 1
    elif len(options) > 2:
        wiki = options[0]
        host = trigger.host
        host = host.split('/')
        x = 1
        status = ''
        while x < len(options):
            status = status + " " + options[x]
            x = x + 1
        cont = 1
    else:
        bot.say(trigger.nick + ": Syntax: .mh wikicode status", trigger.sender)
        cont = 0
    if cont == 1:
        cloakfile = open('/data/project/zppixbot/.sopel/modules/config/cloaks.csv', 'r')
        for line in cloakfile:
            auth = line.split(',')
        if host[0] == auth[0]:
            user = host[1]
            sulgroup = auth[1]
            wiki = [wiki, sulgroup]
            request = [user, status]
            cont = 1
        else:
            bot.say(trigger.nick + ":This service is only avaiable to users with a Miraheze/Wikimedia Cloaks. "
                    + "See phabricator.wikimedia.org/T234716 for updates.", trigger.sender)
            cont = 0
    if cont == 1:
        wikiurl = 'example.org'
        wikiexists = 0
        file = open('/data/project/zppixbot/.sopel/modules/config/statuswikis.csv', 'r')
        for line in file:
            data = line.split(',')
            if data[1] == wiki [0]:
                wikiexists = 1
            if data[1] == wiki[0] and wiki[1] == data[2]:
                wikiurl = data[0]
                site = mwclient.Site(('https', wikiurl), '/w/')
                config = configparser.RawConfigParser()
                config.read('/data/project/zppixbot/.sopel/credentials.txt')
                try:
                    site.login(config.get('zppixbot_status', 'username'), config.get('zppixbot_status', 'password'))
                except errors.LoginError as e:
                    print(e)
                    raise ValueError("Login failed.")
                except requests.exceptions.Timeout:
                    bot.say(trigger.nick + ": We're experinecing delays connecting to that wiki. Try again in a few minutes. If this continues, let us know in #ZppixBot.", trigger.sender)
                except requests.exceptions.TooManyRedirects as e:
                    bot.say(trigger.nick + ": We couldn't connect to that wiki. I've alerted a maintainer in #ZppixBot.", trigger.sender)
                    bot.say("Redirect Error: " + e, '#ZppixBot-logs')
                except requests.exceptions.ConnectionError as e:
                    bot.say(trigger.nick + ": We couldn't connect to that wiki. I've alerted a maintainer in #ZppixBot.", trigger.sender)
                    bot.say("ConnectionError:" + e, '#ZppixBot-logs')
                except requests.exceptions.RequestException as e:
                    bot.say(trigger.nick + ": A fatal error occured. I've alrted a maintainer in #ZppixBot.", trigger.sender)
                    bot.say("Fatal Error: " + e, '#ZppixBot-logs') 
                save_wrap(site, request, bot, trigger)
                cont = 0
        if cont = 1 and wikiexists = 1:
            bot.say(trigger.nick + ": I couldn't authentice you for that wiki.", trigger.sender)
        elif wikiexists = 0:
            bot.say(trigger.nick ": I don't recongise that wiki.", trigger.sender)


@commands('status')
@example('.status mhtest offline')
def status(bot, trigger):
    options = trigger.group(2).split(" ")
    main(bot, trigger, options)
