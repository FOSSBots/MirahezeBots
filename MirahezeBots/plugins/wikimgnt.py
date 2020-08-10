"""wikimgnt.py - interact with Mediawiki API """

from sopel.module import commands, example
from MirahezeBots.utils import mwapihandler as mwapi
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute


class WikimgntSection(StaticSection):
    log_wiki_url = ValidatedAttribute('log_wiki_url', str)
    log_page = ValidatedAttribute('log_page', str)
    wiki_acl = ListAttribute('wiki_acl')
    wiki_farm = ValidatedAttribute('wiki_farm', bool)
    wiki_domain = ValidatedAttribute('wiki_domain', str)
    bot_username = ValidatedAttribute('bot_username', str)
    bot_password = ValidatedAttribute('bot_password', str)


def setup(bot):
    bot.config.define_section('wikimgnt', WikimgntSection)


def configure(config):
    config.define_section('wikimgnt', WikimgntSection, validate=False)
    config.wikimgnt.configure_setting('log_wiki_url', 'What is the URL of the wiki that you would like .log messages to go to? Please specify the URL to that wikis api.php.')
    config.wikimgnt.configure_setting('log_page', 'What page on that wiki would like .log messages to go to? Instead of a space, type a _ please.')
    config.wikimgnt.configure_setting('wiki_acl', 'Please enter NickServ accounts that are allowed to use the commands in this plugin. (No spaces)')
    config.wikimgnt.configure_setting('wiki_farm', 'Are you using this for a wiki farm? (true/false)')
    config.wikimgnt.configure_setting('wiki_domain', 'If you said true to the previous question then What the domain name of your wiki farm? Please specify  the URL to api.php without a subdomain. If you said false, please specify the URL of your wikis api.php.')
    config.wikimgnt.configure_setting('bot_username', 'What is the username the bot should use to login? (from Special:BotPasswords)')
    config.wikimgnt.configure_setting('bot_password', 'What is bot password for the account to login to? (from Special:BotPasswords)')


def blockManager(type, sender, iswikifarm, domain, acl, logininfo, trigger):
    FARMSYNTAX = "Syntax: .{} wiki user reason".format(type)
    SYNTAX = "Syntax: .{} user reason".format(type)
    if sender[1] in acl:
        try:
            options = trigger.group(2).split(" ")
        except Exception:
            if iswikifarm is True:
                return FARMSYNTAX
            else:
                return SYNTAX
        if iswikifarm is False and len(options) < 2:
            return SYNTAX
        elif iswikifarm is True and len(options) < 3:
            return FARMSYNTAX
        elif iswikifarm is True:
            url = 'https://' + options[0] + '.' + domain
            target = options[1]
            reason = options[2]
        else:
            url = domain
            target = options[0]
            reason = options[1]
        response = mwapi.main(sender[0], target, type, reason, url, logininfo[0], logininfo[1])
        return response
    else:
        return "Sorry: you don't have permission to use this plugin"


@commands('log')
@example('.log restarting sopel')
def logpage(bot, trigger):
    """Log given message to configured page"""
    if trigger.account in bot.settings.wikimgnt.wiki_acl:
        sender = trigger.nick
        url = bot.settings.wikimgnt.log_wiki_url
        target = bot.settings.wikimgnt.log_page
        if trigger.group(2) is None:
            bot.say("Syntax: .log message")
        else:
            message = trigger.group(2)
            response = mwapi.main(sender, target, 'edit', message, url, bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password)
            bot.reply(response)
    else:
        bot.reply("Sorry: you don't have permission to use this plugin")


@commands('deletepage')
@example('.deletepage Test_page vandalism')
@example('.deletepage test Test_page vandalism')
def deletepage(bot, trigger):
    """Delete the given page (depending on config, on the given wiki)"""
    if trigger.account in bot.settings.wikimgnt.wiki_acl:
        sender = trigger.nick
        try:
            options = trigger.group(2).split(" ")
        except Exception:
            if bot.settings.wikimgnt.wiki_farm is True:
                bot.say("Syntax: .deletepage wiki page reason")
            else:
                bot.say("Syntax: .deletepage page reason")
            return
        if bot.settings.wikimgnt.wiki_farm is False and len(options) < 2:
            bot.say("Syntax: .deletepage page reason")
            return
        elif bot.settings.wikimgnt.wiki_farm is True and len(options) < 3:
            bot.say("Syntax: .deletepage wiki page reason")
            return
        elif bot.settings.wikimgnt.wiki_farm is True:
            url = 'https://' + options[0] + '.' + bot.settings.wikimgnt.wiki_domain
        else:
            url = bot.settings.wikimgnt.wiki_domain
        target = options[0]
        reason = options[1]
        response = mwapi.main(sender, target, 'delete', reason, url, bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password)
        bot.reply(response)
    else:
        bot.reply("Sorry: you don't have permission to use this plugin")


@commands('block')
@example('.block Zppix vandalism')
@example('.block test Zppix vandalism')
def blockuser(bot, trigger):
    """Block the given user indefinitely (depending on config, on the given wiki)"""
    replytext = blockManager("block", [trigger.nick, trigger.account], bot.settings.wikimgnt.wiki_farm, bot.settings.wikimgnt.wiki_domain, bot.settings.wikimgnt.wiki_acl, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password], trigger)
    bot.reply(replytext)


@commands('unblock')
@example('.unblock Zppix appeal')
@example('.unblock test Zppix per appeal')
def unblockuser(bot, trigger):
    """Unblock the given user (depending on config, on the given wiki)"""
    replytext = blockManager("unblock", [trigger.nick, trigger.account], bot.settings.wikimgnt.wiki_farm, bot.settings.wikimgnt.wiki_domain, bot.settings.wikimgnt.wiki_acl, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password], trigger)
    bot.reply(replytext)
