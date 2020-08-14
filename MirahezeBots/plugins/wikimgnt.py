"""wikimgnt.py - interact with Mediawiki API """

from sopel.module import commands, example, require_admin
from MirahezeBots.utils import mwapihandler as mwapi
from sopel.config.types import StaticSection, ValidatedAttribute, ListAttribute
from sopel.tools import get_logger, SopelMemory
from sopel.config import ConfigurationError
from MirahezeBots.utils import jsonparser as jp
LOGGER = get_logger('wikimgnt')


ACLERROR = "Sorry, you don't have permissions to use this plugin on that wiki"


class WikimgntSection(StaticSection):
    log_page = ValidatedAttribute('log_page', str)
    wiki_acl = ListAttribute('wiki_acl')
    datafile = ValidatedAttribute('datafile', str)
    wiki_farm = ValidatedAttribute('wiki_farm', bool)
    wiki_domain = ValidatedAttribute('wiki_domain', str)
    bot_username = ValidatedAttribute('bot_username', str)
    bot_password = ValidatedAttribute('bot_password', str)


def setup(bot):
    bot.config.define_section('wikimgnt', WikimgntSection)
    if bot.settings.wikimgnt.datafile and bot.settings.wikimgnt.wiki_acl:
        raise ConfigurationError("Use of wiki_acl and datafile together is not supported")
    elif bot.settings.wikimgnt.datafile and bot.settings.wikimgnt.wiki_farm is False:
        raise ConfigurationError("For single wikis you must use wiki_acl")
    elif bot.settings.wikimgnt.wiki_acl and bot.settings.wikimgnt.wiki_farm is True:
        raise ConfigurationError("For wikifarms you must use datafile")
    elif bot.settings.wikimgnt.wiki_farm is True and bot.settings.wikimgnt.log_page:
        LOGGER.warn("For wikifarms, log_page does not need to be defined in the config")
    elif bot.settings.wikimgnt.wiki_farm is False and bot.settings.wikimgnt.log_page is None:
        raise ConfigurationError("For single wikis, log_page must be defined")
    elif bot.settings.wikimgnt.datafile:
        bot.memory["wikimgnt"] = SopelMemory()
        bot.memory["wikimgnt"]["jdcache"] = jp.createdict(bot.settings.wikimgnt.datafile)


def configure(config):
    config.define_section('wikimgnt', WikimgntSection, validate=False)
    config.wikimgnt.configure_setting('log_page', 'What page on your wiki would like .log messages to go to? Instead of a space, type a _ please.')
    config.wikimgnt.configure_setting('wiki_acl', 'Please enter NickServ accounts that are allowed to use the commands in this plugin. (No spaces)')
    config.wikimgnt.configure_setting('datafile', 'What is the path to the wikimgnt datafile')
    config.wikimgnt.configure_setting('wiki_farm', 'Are you using this for a wiki farm? (true/false)')
    config.wikimgnt.configure_setting('wiki_domain', 'If you said true to the previous question then What the domain name of your wiki farm? Please specify  the URL to api.php without a subdomain. If you said false, please specify the URL of your wikis api.php.')
    config.wikimgnt.configure_setting('bot_username', 'What is the username the bot should use to login? (from Special:BotPasswords)')
    config.wikimgnt.configure_setting('bot_password', 'What is bot password for the account to login to? (from Special:BotPasswords)')


def get_logpage(wiki, jsondata):
    if wiki in jsondata["wikis"].keys():
        return jsondata["wikis"][wiki]["log_page"]


def check_access(acldata, requestdata,):
    if requestdata[1] in acldata["wikis"].keys():
        sulgroup = acldata["wikis"][requestdata[1]]["sulgroup"]
    else:
        return "Wiki could not be found"
    if requestdata[0] in acldata["users"].keys():
        if sulgroup in acldata["users"][requestdata[0]]["groups"].keys():
            return True
        else:
            return False
    else:
        return False


def block_manager(type, sender, siteinfo, logininfo, trigger, acl=None):
    FARMSYNTAX = "Syntax: .{} wiki user reason".format(type)
    SYNTAX = "Syntax: .{} user reason".format(type)
    try:
        options = trigger.group(2).split(" ")
    except Exception:
        if siteinfo[2] is True:
            return FARMSYNTAX
        else:
            return SYNTAX
    if siteinfo[2] is False and len(options) < 2:
        return SYNTAX
    elif siteinfo[2] is True and len(options) < 3:
        return FARMSYNTAX
    elif siteinfo[2] is True:
        url = 'https://' + options[0] + '.' + siteinfo[0]
        target = options[1]
        reason = options[2]
        requestdata = [trigger.account, options[0]]
        if check_access(siteinfo[1], requestdata) is not True:
            return ACLERROR
    elif siteinfo[2] is False:
        url = siteinfo[0]
        target = options[0]
        reason = options[1]
        if trigger.account not in acl:
            return ACLERROR
    response = mwapi.main(sender[0], target, type, reason, url, [logininfo[0], logininfo[1]])
    return response


@commands('log')
@example('.log restarting sopel')
def logpage(bot, trigger):
    """Log given message to configured page"""
    try:
        options = trigger.group(2).split(" ")
    except Exception:
        if bot.settings.wikimgnt.wiki_farm is False:
            bot.say("Syntax: .log message")
            return
        elif bot.settings.wikimgnt.wiki_farm is True:
            bot.say("Syntax: .log wiki message")
            return
    sender = trigger.nick
    if bot.settings.wikimgnt.wiki_farm is True and len(options) < 2:
        bot.say("Syntax: .log wiki message")
        return
    elif bot.settings.wikimgnt.wiki_farm is True:
        url = 'https://' + options[0] + '.' + bot.settings.wikimgnt.wiki_domain
        message = options[1]
        target = get_logpage(options[0], bot.memory["wikimgnt"]["jdcache"])
        requestdata = [trigger.account, options[0]]
        if check_access(bot.memory["wikimgnt"]["jdcache"], requestdata) is not True:
            bot.reply(ACLERROR)
            return
    else:
        url = bot.settings.wikimgnt.wiki_domain
        message = options[0]
        target = bot.settings.wikimgnt.log_page
        if trigger.account not in bot.settings.wikimgnt.wiki_acl:
            bot.reply(ACLERROR)
            return
    response = mwapi.main(sender, target, 'edit', message, url, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password])
    bot.reply(response)


@commands('deletepage')
@example('.deletepage Test_page vandalism')
@example('.deletepage test Test_page vandalism')
def deletepage(bot, trigger):
    """Delete the given page (depending on config, on the given wiki)"""
    sender = trigger.nick
    try:
        options = trigger.group(2).split(" ")
    except Exception:
        if bot.settings.wikimgnt.wiki_farm is True:
            bot.say("Syntax: .deletepage wiki page reason")
        else:
            bot.say("Syntax: .deletepage page reason")
        return
    if bot.settings.wikimgnt.wiki_farm is True:
        requestdata = [trigger.account, options[0]]
        if check_access(bot.memory["wikimgnt"]["jdcache"], requestdata) is not True:
            bot.reply(ACLERROR)
            return
        url = 'https://' + options[0] + '.' + bot.settings.wikimgnt.wiki_domain
        target = options[1]
        reason = options[2]
    elif bot.settings.wikimgnt.wiki_farm is False:
        if trigger.account not in bot.settings.wikimgnt.wiki_acl:
            bot.reply(ACLERROR)
            return
        url = bot.settings.wikimgnt.wiki_domain
        target = options[0]
        reason = options[1]
    if bot.settings.wikimgnt.wiki_farm is False and len(options) < 2:
        bot.say("Syntax: .deletepage page reason")
        return
    elif bot.settings.wikimgnt.wiki_farm is True and len(options) < 3:
        bot.say("Syntax: .deletepage wiki page reason")
        return
    response = mwapi.main(sender, target, 'delete', reason, url, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password])
    bot.reply(response)


@commands('block')
@example('.block Zppix vandalism')
@example('.block test Zppix vandalism')
def blockuser(bot, trigger):
    """Block the given user indefinitely (depending on config, on the given wiki)"""
    siteinfo = [bot.settings.wikimgnt.wiki_domain, bot.memory["wikimgnt"]["jdcache"], bot.settings.wikimgnt.wiki_farm]
    if bot.settings.wikimgnt.wiki_acl:
        replytext = block_manager("block", [trigger.nick, trigger.account], siteinfo, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password], trigger, bot.settings.wikimgnt.wiki_acl)
    else:
        replytext = block_manager("block", [trigger.nick, trigger.account], siteinfo, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password], trigger)
    bot.reply(replytext)


@commands('unblock')
@example('.unblock Zppix appeal')
@example('.unblock test Zppix per appeal')
def unblockuser(bot, trigger):
    """Unblock the given user (depending on config, on the given wiki)"""
    siteinfo = [bot.settings.wikimgnt.wiki_domain, bot.memory["wikimgnt"]["jdcache"], bot.settings.wikimgnt.wiki_farm]
    if bot.settings.wikimgnt.wiki_acl:
        replytext = block_manager("unblock", [trigger.nick, trigger.account], siteinfo, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password, ], trigger, bot.settings.wikimgnt.wiki_acl)
    else:
        replytext = block_manager("unblock", [trigger.nick, trigger.account], siteinfo, [bot.settings.wikimgnt.bot_username, bot.settings.wikimgnt.bot_password], trigger)
    bot.reply(replytext)


@require_admin(message="Only admins may purge cache.")
@commands('resetwikimgntcache')
def reset_wikimgnt_cache(bot, trigger):
    """
    Reset the cache of the wiki management data file
    """
    bot.reply("Refreshing Cache...")
    bot.memory["wikimgnt"]["jdcache"] = jp.createdict(bot.settings.wikimgnt.datafile)
    bot.reply("Cache refreshed")


@require_admin(message="Only admins may check cache")
@commands('checkwikimgntcache')
def check_wikimgnt_cache(bot, trigger):
    """
    Validate the cache matches the copy on disk
    """
    result = jp.validatecache(bot.settings.wikimgnt.datafile, bot.memory["wikimgnt"]["jdcache"])
    if result:
        bot.reply("Cache is correct.")
    else:
        bot.reply("Cache does not match on-disk copy")
