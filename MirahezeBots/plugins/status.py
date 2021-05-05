"""status.py - Mediawiki Status Page Updater."""

from MirahezeBots_jsonparser import jsonparser as jp
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example, require_admin
from sopel.tools import SopelMemory

from MirahezeBots.utils import mwapihandler as mwapi

pages = ''


class StatusSection(StaticSection):
    """Create configuration for Sopel."""

    datafile = ValidatedAttribute('datafile', str)
    bot_username = ValidatedAttribute('bot_username', str)
    bot_password = ValidatedAttribute('bot_password', str)
    support_channel = ValidatedAttribute('support_channel', str)


def setup(bot):
    """Set up the config section & memory."""
    bot.config.define_section('status', StatusSection)
    bot.memory['status'] = SopelMemory()
    bot.memory['status']['jdcache'] = jp.createdict(bot.settings.status.datafile)


def configure(config):
    """Set up the configuration options."""
    config.define_section('status', StatusSection, validate=False)
    config.status.configure_setting(
        'datafile',
        'What is the status data file?',
    )
    config.status.configure_setting(
        'bot_username',
        'What is the statusbot username? (from Special:BotPasswords)',
    )
    config.status.configure_setting(
        'bot_password',
        "What is the statusbot accounts's bot password? (from Special:BotPasswords)",
    )
    config.status.configure_setting(
        'support_channel',
        'Specify a support IRC channel (leave blank for none).',
    )


def updatestatus(requestdata, authinfo, acldata, supportchan, session):
    """Update the /Status page of a user."""
    if requestdata[2] in acldata['wikis']:
        wikiurl = str('https://' + acldata['wikis'][requestdata[2]]['url'] + '/w/api.php')
        sulgroup = acldata['wikis'][requestdata[2]]['sulgroup']
    else:
        return 'Wiki could not be found'
    if requestdata[0] in acldata['users']:
        if sulgroup in acldata['users'][requestdata[0]]['groups']:
            request = [acldata['users'][requestdata[0]]['groups'][sulgroup], requestdata[3]]
        else:
            return f"Data not found for {sulgroup} in {requestdata[0]}, Keys were: {acldata['users'][requestdata[0]].keys()}"
    elif requestdata[1][0] in acldata['sulgroups'][sulgroup]['cloaks']:
        request = [requestdata[1][1], requestdata[3]]
    else:
        ERRNOAUTH = "You don't seem to be authorised to use this plugin. Check you are signed into NickServ and try again."
        if supportchan is None:
            return ERRNOAUTH
        return f'{ERRNOAUTH} If this persists, ask for help in {supportchan}.'
    return mwapi.main(
        performer=request[0],
        target=str('User:' + (str(request[0]) + '/Status')),
        action='create',
        reason=str('Updating status to ' + str(request[1]) + ' per ' + str(request[0])),
        url=wikiurl,
        authinfo=[authinfo[0], authinfo[1]],
        content=str(request[1]),
        session=session,
    )


@commands('status')
@example('.status mhtest offline')
def changestatus(bot, trigger):
    """Update the /Status subpage of Special:MyPage on the indicated wiki."""
    options = []
    try:
        options = trigger.group(2).split(' ')
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
                status = status + ' ' + options[x]
                x = x + 1
            cont = 1
        else:
            bot.reply('Syntax: .status wikicode new-status')
            cont = 0
    except AttributeError as e:
        bot.reply('Syntax: .status wikicode new-status')
        bot.say(f'AttributeError: {e} from Status plugin in {trigger.sender}', bot.config.core.logging_channel)
        cont = 0
    if cont == 1:
        requestdata = [str(trigger.account), host, wiki, str(status)]
        response = updatestatus(
            requestdata,
            [bot.settings.status.bot_username, bot.settings.status.bot_password],
            bot.memory['status']['jdcache'],
            bot.settings.status.support_channel,
            bot.memory['shared']['session'],
        )
        if response == 'create request sent. You may want to check the create log to be sure that it worked.':
            bot.reply('Success')
        else:
            bot.reply(str(response))


@require_admin(message='Only admins may purge cache.')
@commands('resetstatuscache')
def reset_status_cache(bot, trigger):  # noqa: U100
    """Reset the cache of the channel management data file."""
    bot.reply('Refreshing Cache...')
    bot.memory['status']['jdcache'] = jp.createdict(bot.settings.status.datafile)
    bot.reply('Cache refreshed')


@require_admin(message='Only admins may check cache')
@commands('checkstatuscache')
def check_status_cache(bot, trigger):  # noqa: U100
    """Validate the cache matches the copy on disk."""
    result = jp.validatecache(bot.settings.status.datafile, bot.memory['status']['jdcache'])
    if result:
        bot.reply('Cache is correct.')
    else:
        bot.reply('Cache does not match on-disk copy')
