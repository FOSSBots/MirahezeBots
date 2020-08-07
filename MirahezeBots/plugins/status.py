''' status.py - Mediawiki Status Page Updater '''

import requests
import time

from sopel.module import commands, example
from sopel.config.types import StaticSection, ValidatedAttribute
from MirahezeBots.utils import mwapihandler as mwapi


pages = ''


class StatusSection(StaticSection):
    data_path = ValidatedAttribute('data_path', str)
    bot_username = ValidatedAttribute('bot_username', str)
    bot_password = ValidatedAttribute('bot_password', str)
    support_channel = ValidatedAttribute('support_channel', str)


def setup(bot):
    bot.config.define_section('status', StatusSection)


def configure(config):
    config.define_section('status', StatusSection, validate=False)
    config.status.configure_setting('data_path', 'What is the path to the statusbot data files?')
    config.status.configure_setting('bot_username', 'What is the statusbot username? (from Special:BotPasswords)')
    config.status.configure_setting('bot_password', "What is the statusbot accounts's bot password? (from Special:BotPasswords)")
    config.status.configure_setting('support_channel', 'Specify a support IRC channel (leave blank for none).')


def updatestatus(bot, requestdata):
    cont = 0
    cloakfile = open(bot.config.status.data_path + 'cloaks.csv', 'r')
    for line in cloakfile:
        auth = line.split(',')
        if requestdata[1][0] == auth[0]:
            user = requestdata[1][1]
            sulgroup = auth[1]
            wiki = [requestdata[2], sulgroup]
            request = [user, requestdata[3]]
            cont = 1
            break
    if cont == 0:
        usersfile = open(bot.config.status.data_path + 'users.csv', 'r')
        for line in usersfile:
            auth = line.split(',')
            if requestdata[1][0] == auth[0]:
                user = auth[1]
                sulgroup = auth[2]
                wiki = [requestdata[2], sulgroup]
                request = [user, requestdata[3]]
                cont = 1
                break
    if cont == 0:
        message = "You don't seem to be authorised to use this module. Please check you are signed into NickServ and try again."
        if bot.config.status.support_channel is not None:
            message = message + " If this persists, ask for help in {}".format(bot.config.status.support_channel)
        return message
    if cont == 1:
        wikiurl = 'example.org'
        wikiexists = 0
        file = open(bot.config.status.data_path + 'statuswikis.csv', 'r')
        for line in file:
            data = line.split(',')
            if data[1] == wiki[0]:
                wikiexists = 1
            if data[1] == wiki[0] and wiki[1] == data[2]:
                wikiurl = "https://" + str(data[0]) + "/w/api.php"
                content = mwapi.main(performer=request[0], target=str("User:" + (str(request[0]) + "/Status")),
                                     action="create", reason=str("Updating status to " + str(request[1]) + " per " + str(request[0])), url=wikiurl, username=bot.settings.status.bot_username, password=bot.settings.status.bot_password, content=str(request[1]))
                return content
        if cont == 1 and wikiexists == 1:
            return "I couldn't authentice you for that wiki."
        elif wikiexists == 0:
            return "I don't recongise that wiki."


@commands('status')
@example('.status mhtest offline')
def status(bot, trigger):
    """Update's the /Status subpage of Special:MyPage on the indicated wiki"""
    options = []
    try:
        options = trigger.group(2).split(" ")
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
            bot.reply("Syntax: .status wikicode new-status")
            cont = 0
    except AttributeError as e:
        bot.reply("Syntax: .status wikicode new-status")
        bot.say("AttributeError: {} from Status plugin in {}".format(e, trigger.sender), bot.config.core.logging_channel)
        cont = 0
    if cont == 1:
        requestdata = [str(trigger.account), host, wiki, str(status)]
        response = updatestatus(bot, requestdata)
        if response == "create request sent. You may want to check the create log to be sure that it worked.":
            bot.reply("Success")
        else:
            bot.reply(str(response))
