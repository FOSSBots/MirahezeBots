from __future__ import unicode_literals, absolute_import, print_function, division

import configparser
import json
import mwclient
import requests
import re
import time

from mwclient import errors

from sopel.module import rule, commands, example
from sopel.config.types import StaticSection, ValidatedAttribute


pages = ''


class StatusSection(StaticSection):
    data_path = ValidatedAttribute('data_path', str)
    wiki_username = ValidatedAttribute('wiki_username', str)
    wiki_password = ValidatedAttribute('wiki_password', str)
    support_channel = ValidatedAttribute('support_channel', str)


def setup(bot):
    bot.config.define_section('status', StatusSection)


def configure(config):
    config.define_section('status', StatusSection, validate=False)
    config.status.configure_setting('data_path', 'What is the path to the statusbot data files?')
    config.status.configure_setting('wiki_username', 'What is the statusbot wiki username? (from Special:BotPasswords)')
    config.status.configure_setting('wiki_password', 'What is the statusbot wiki password? (from Special:BotPasswords)')
    config.status.configure_setting('support_channel', 'Specify a support IRC channel (leave blank for none).')


def save_wrap(site, request, bot, trigger):
    pagename = 'User:' + request[0] + '/Status'
    bot.reply("Updating " + pagename + " to " + request[1] + "!")
    page = site.Pages[pagename]
    save_edit(page, request[1], bot, trigger)


def save_edit(page, status, bot, trigger):
    time.sleep(5)
    edit_summary = "BOT: Setting Status to: " + status + " per " \
                   + trigger.hostmask
    times = 0
    while True:
        if times > 1:
            break
        try:
            page.save(status, summary=edit_summary, bot=True, minor=True)
            bot.reply("Updated!")
        except errors.ProtectedPageError:
            print('Could not edit ' + page + ' due to protection')
            bot.reply("Error: Page Protected")
            times += 1
        except errors.EditError:
            print("Error")
            bot.reply("An Error Occurred :(")
            times += 1
            time.sleep(5)  # sleep for 5 seconds before trying again
            continue
        except errors.UserBlocked:
            bot.reply("StatusBot is currently unavailable for that wiki. Our team are working on it!")
            bot.say("ERR: The bot is blocked on " + str(page), 'bot.config.core.logging_channel')
        except requests.exceptions.Timeout:
            bot.reply("We're experinecing delays "
                      + "connecting to that wiki. Try again in a few minutes.")
            if bot.config.status.support_channel is not None:
                bot.say("If this continues, let us know in {}".format(bot.config.status.support_channel))
        except requests.exceptions.TooManyRedirects as e:
            bot.reply("We couldn't connect to that wiki.")
            if bot.config.status.support_channel is not None:
                bot.say("I've alerted a maintainer in {}".format(bot.config.status.support_channel))
            print(e)
            raise ValueError("Redirect error")
        except requests.exceptions.ConnectionError as e:
            bot.reply("We couldn't connect to that wiki.")
            if bot.config.status.support_channel is not None:
                bot.say("I've alerted a maintainer in {}".format(bot.config.status.support_channel))
            print(e)
            raise ValueError("Connection error")
        except requests.exceptions.RequestException as e:
            bot.reply("A fatal error occured.")
            if bot.config.status.support_channel is not None:
                bot.say("I've alerted a maintainer in {}".format(bot.config.status.support_channel))
            print(e)
            raise ValueError("Fatal error")
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
        status = options[1]
        x = 2
        while x < len(options):
            status = status + " " + options[x]
            x = x + 1
        cont = 1
    else:
        bot.reply("Syntax: .status wikicode status")
        cont = 0
    if cont == 1:
        cont = 0
        cloakfile = open(bot.config.status.data_path
                         + 'cloaks.csv', 'r')
        for line in cloakfile:
            auth = line.split(',')
            if host[0] == auth[0]:
                user = host[1]
                sulgroup = auth[1]
                wiki = [wiki, sulgroup]
                request = [user, status]
                cont = 1
                break
        if cont == 0:
            usersfile = open(bot.config.status.data_path
                             + 'users.csv', 'r')
            for line in usersfile:
                auth = line.split(',')
                if str(trigger.account) == auth[0]:
                    user = auth[1]
                    sulgroup = auth[2]
                    wiki = [wiki, sulgroup]
                    request = [user, status]
                    cont = 1
                    break
        if cont == 0:
            bot.reply("You don't seem to be authorised to use this module."
                      + " Please check you are signed into NickServ and try again.", trigger.sender)
            if bot.config.status.support_channel is not None:
                bot.say("If this persists, ask for help in {}".format(bot.config.status.support_channel))
            cont = 0
    if cont == 1:
        wikiurl = 'example.org'
        wikiexists = 0
        file = open(bot.config.status.data_path
                    + 'statuswikis.csv', 'r')
        for line in file:
            data = line.split(',')
            if data[1] == wiki[0]:
                wikiexists = 1
            if data[1] == wiki[0] and wiki[1] == data[2]:
                wikiurl = data[0]
                site = mwclient.Site((wikiurl), path='/w/')
                try:
                    site.login(bot.config.status.wiki_username,
                               bot.config.status.wiki_password)
                except errors.LoginError as e:
                    print(e)
                    raise ValueError("Login failed.")
                except requests.exceptions.Timeout:
                    bot.reply("We're experinecing delays "
                              + "connecting to that wiki. Try again in a few minutes.")
                    if bot.config.status.support_channel is not None:
                        bot.say("If this continues, let us know in {}".format(bot.config.status.support_channel))
                except requests.exceptions.TooManyRedirects as e:
                    bot.reply("We couldn't connect to that wiki.")
                    if bot.config.status.support_channel is not None:
                        bot.say("I've alerted a maintainer in {}".format(bot.config.status.support_channel))
                    print(e)
                    raise ValueError("Redirect error")
                except requests.exceptions.ConnectionError as e:
                    bot.reply("We couldn't connect to that wiki.")
                    if bot.config.status.support_channel is not None:
                        bot.say("I've alerted a maintainer in {}".format(bot.config.status.support_channel))
                    print(e)
                    raise ValueError("Connection error")
                except requests.exceptions.RequestException as e:
                    bot.reply("A fatal error occured.")
                    if bot.config.status.support_channel is not None:
                        bot.say("I've alerted a maintainer in {}".format(bot.config.status.support_channel))
                    print(e)
                    raise ValueError("Fatal error")
                save_wrap(site, request, bot, trigger)
                cont = 0
        if cont == 1 and wikiexists == 1:
            bot.reply("I couldn't authentice you for that wiki.")
        elif wikiexists == 0:
            bot.reply("I don't recongise that wiki.")


@commands('status')
@example('.status mhtest offline')
def status(bot, trigger):
    """Update's the /Status subpage of Special:MyPage on the indicated wiki"""
    options = trigger.group(2).split(" ")
    main(bot, trigger, options)
