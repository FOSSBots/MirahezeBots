# -*- coding: utf-8 -*-
"""
rss.py - Sopel rss plugins
Copyright © 2016, RebelCodeBase, https://github.com/RebelCodeBase/sopel-rss
Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3

This module posts rss feed items to irc channels
"""
import hashlib
import shlex
import time
import urllib.parse
import urllib.request

import feedparser
from sopel.config.types import ListAttribute, StaticSection
from sopel.logger import get_logger
from sopel.module import commands, example, interval, require_admin
from sopel.tools import SopelMemory

LOGGER = get_logger(__name__)

MAX_HASHES_PER_FEED = 300

UPDATE_INTERVAL = 60  # seconds

ESCAPE_CHARACTER = '%'

ESCAPE_COLOR = '\x03'

ESCAPE_CODE = {
    '00': '00',
    '01': '01',
    '02': '02',
    '03': '03',
    '04': '04',
    '05': '05',
    '06': '06',
    '07': '07',
    '08': '08',
    '09': '09',
    '10': '10',
    '11': '11',
    '12': '12',
    '13': '13',
    '14': '14',
    '15': '15',
    '16': '\x02',
    '17': '\x1d',
    '18': '\x1f',
    '19': '\x16',
    '20': '\x0f',
}

COLOR = {
    '00': 'white',
    '01': 'black',
    '02': 'blue',
    '03': 'green',
    '04': 'red',
    '05': 'brown',
    '06': 'purple',
    '07': 'orange',
    '08': 'yellow',
    '09': 'lime',
    '10': 'cyan',
    '11': 'aqua',
    '12': 'azure',
    '13': 'pink',
    '14': 'grey',
    '15': 'silver',
    '16': 'bold',
    '17': 'italic',
    '18': 'underline',
}

FOREGROUND = {
    '00': '01',
    '01': '00',
    '02': '00',
    '03': '00',
    '04': '01',
    '05': '00',
    '06': '00',
    '07': '01',
    '08': '01',
    '09': '01',
    '10': '00',
    '11': '01',
    '12': '01',
    '13': '01',
    '14': '00',
    '15': '01',
    '16': '00',
    '17': '01',
    '18': '00',
}

BACKGROUND = {
    '00': '00',
    '01': '01',
    '02': '02',
    '03': '03',
    '04': '04',
    '05': '05',
    '06': '06',
    '07': '07',
    '08': '08',
    '09': '09',
    '10': '10',
    '11': '11',
    '12': '12',
    '13': '13',
    '14': '14',
    '15': '15',
    '16': '01',
    '17': '00',
    '18': '01',
}

CONFIG_SEPARATOR = ';'

FORMAT_SEPARATOR = '+'

FORMAT_DEFAULT = 'fl+ftl'

TEMPLATE_SEPARATOR = '|'

TEMPLATES_DEFAULT = {
    'f': ESCAPE_CHARACTER + '16[{}]' + ESCAPE_CHARACTER + '16',
    'a': '<{}>',
    'd': '{}',
    'g': '{}',
    'l': ESCAPE_CHARACTER + '16→' + ESCAPE_CHARACTER + '16 {}',
    'p': '({})',
    's': '{}',
    't': '{}',
    'y': ESCAPE_CHARACTER + '16→' + ESCAPE_CHARACTER + '16 {}',
}

COMMANDS = {
    'add': {
        'synopsis': 'synopsis: {}rss add <channel> <name> <url> [<options>]',
        'helptext': ['add a feed identified by <name> with feed address <url> to irc channel <channel>. optional: add a format string.'],
        'examples': ['{}rss add #sopel-test guardian https://www.theguardian.com/world/rss',
                     '{}rss add #sopel-test guardian https://www.theguardian.com/world/rss f=' + FORMAT_DEFAULT],
        'required': 3,
        'optional': 1,
        'function': '_rss_add'
    },
    'colors': {
        'synopsis': 'synopsis: {}rss colors',
        'helptext': ['show color and format codes.'],
        'examples': [''],
        'required': 0,
        'optional': 0,
        'function': '_rss_colors'
    },
    'config': {
        'synopsis': 'synopsis: {}rss config <key> [<value>]',
        'helptext': ['show the value of a key in the config file or set the value of a key in the config file.'],
        'examples': ['{}rss config formats',
                     '{}rss config templates'],
        'required': 1,
        'optional': 1,
        'function': '_rss_config'
    },
    'del': {
        'synopsis': 'synopsis: {}rss del <name>',
        'helptext': ['delete a feed identified by <name>.'],
        'examples': ['{}rss del guardian'],
        'required': 1,
        'optional': 0,
        'function': '_rss_del'
    },
    'fields': {
        'synopsis': 'synopsis: {}rss fields <name>',
        'helptext': ['list all feed item fields available for the feed identified by <name>.',
                     'f: feedname, a: author, d: description, g: guid, l: link, p: published, s: summary, t: title, y: tinyurl'],
        'examples': ['{}rss fields guardian'],
        'required': 1,
        'optional': 0,
        'function': '_rss_fields'
    },
    'formats': {
        'synopsis': 'synopsis: {}rss format <name> [f=<format>]',
        'helptext': ['get the format string for the feed identified by <name>.',
                     'or set the format string for the feed identified by <name>.',
                     'a format string begins with "f=" and it is separated by the separator "' + FORMAT_SEPARATOR + '"',
                     'the left part of the format string indicates the fields that will be hashed for an item. if you change this part all feed items will be reposted.',
                     'the fields determine when a feed item will be reposted. if you see duplicates then first look at this part of the format string.',
                     'the right part of the format string determines which feed item fields will be posted.'],
        'examples': ['{}rss formats f=fl+ftl'],
        'required': 1,
        'optional': 1,
        'function': '_rss_formats'
    },
    'get': {
        'synopsis': 'synopsis: {}rss get <name>',
        'helptext': ['post all feed items of the feed identified by <name> to its channel.'],
        'examples': ['{}rss get guardian'],
        'required': 1,
        'optional': 0,
        'function': '_rss_get'
    },
    'help': {
        'synopsis': 'synopsis: {}rss help [<command>]',
        'helptext': ['get help for <command>.'],
        'examples': ['{}rss help format'],
        'required': 0,
        'optional': 2,
        'function': '_rss_help'
    },
    'join': {
        'synopsis': 'synopsis: {}rss join',
        'helptext': ['join all channels which are associated to a feed.'],
        'examples': ['{}rss join'],
        'required': 0,
        'optional': 0,
        'function': '_rss_join'
    },
    'list': {
        'synopsis': 'synopsis: {}rss list [<feed>|<channel>]',
        'helptext': ['list the properties of a feed identified by <feed> or list all feeds in a channel identified by <channel>.'],
        'examples': ['{}rss list', '{}rss list guardian',
                     '{}rss list', '{}rss list #sopel-test'],
        'required': 0,
        'optional': 1,
        'function': '_rss_list'
    },
    'templates': {
        'synopsis': 'synopsis: {}rss templates <name> [t=<field>' + TEMPLATE_SEPARATOR + '<template>]',
        'helptext': ['get the templates for the feed identified by <name>.',
                     'or set the templates for the feed identified by <name>.',
                     'a template is separated by the separator "' + CONFIG_SEPARATOR + '", multiple templates are separated by the separator "' + TEMPLATE_SEPARATOR + '"',
                     'the left part of the template is the field for which the output will be overridden.',
                     'the right part is the actual template string. Curly brackets {} will be replaced by the value of the field.'],
        'examples': ['{}rss templates t=l' + TEMPLATE_SEPARATOR + '-> {}' + CONFIG_SEPARATOR + 't=y' + TEMPLATE_SEPARATOR + '-> {}'],
        'required': 1,
        'optional': 1,
        'function': '_rss_templates'
    },
    'update': {
        'synopsis': 'synopsis: {}rss update',
        'helptext': ['post the latest feed items of all feeds.'],
        'examples': ['{}rss update'],
        'required': 0,
        'optional': 0,
        'function': '_rss_update'
    }
}

CONFIG = {
    'feeds': {
        'synopsis': 'feeds = <channel1>|<feed1>|<url1>[|<format1>],<channel2>|<feed2>|<url2>[|<format2>],...',
        'helptext': ['the bot is watching these feeds. it reads the feed located at the url and posts new feed items to the channel in the specified format.'],
        'examples': ['feeds = #sopel-test|guardian|https://www.theguardian.com/world/rss|fl+ftl'],
        'func_get': '_config_get_feeds',
        'func_set': '_config_set_feeds'
    },
    'formats': {
        'synopsis': 'formats = f=<format1>;f=<format2>,...',
        'helptext': ['if no format is defined for a feed the bot will try these formats and the global default format (' + FORMAT_DEFAULT + ') one by one until it finds a valid format.',
                     'a format is valid if the fields used in the format do exist in the feed items.'],
        'examples': ['formats = f=l+fpatl' + CONFIG_SEPARATOR + 'f=l+fptl'],
        'func_get': '_config_get_formats',
        'func_set': '_config_set_formats'
    },
    'templates': {
        'synopsis': 'templates = t=<field1>' + TEMPLATE_SEPARATOR + '<template1>' + CONFIG_SEPARATOR + 't=<field2>' + TEMPLATE_SEPARATOR + '<template2>,...',
        'helptext': ['for each rss feed item field a template can be defined which will be used to create the output string.',
                     'each template must contain exactly one pair of curly brackets which will be replaced by the field value.',
                     'the bot will use the global default template for those fields which no custom template is defined.'],
        'examples': ['templates = t=t' + TEMPLATE_SEPARATOR + '«{}»'],
        'func_get': '_config_get_templates',
        'func_set': '_config_set_templates'
    },
}

MESSAGES = {
    'added_feed_formater_for_feed':
        'added feed formater for feed "{}"',
    'added_ring_buffer_for_feed':
        'added ring buffer for feed "{}"',
    'added_rss_feed_to_channel_with_url':
        'added rss feed "{}" to channel "{}" with url "{}"',
    'added_rss_feed_to_channel_with_url_and_options':
        'added rss feed "{}" to channel "{}" with url "{}" and options "{}"',
    'added_sqlite_table_for_feed':
        'added sqlite table "{}" for feed "{}"',
    'channel_must_start_with_a_hash_sign':
        'channel "{}" must start with a "#"',
    'command_is_one_of':
        'where <command> is one of {}',
    'consider_rss_fields':
        'consider {}rss fields {} to create a valid format',
    'deleted_ring_buffer_for_feed':
        'deleted ring buffer for feed "{}"',
    'deleted_rss_feed_in_channel_with_url':
        'deleted rss feed "{}" in channel "{}" with url "{}"',
    'dropped_sqlite_table_of_feed':
        'dropped sqlite table "{}" of feed "{}"',
    'examples':
        'examples:',
    'feed_items_have_neither_title_nor_description':
        'feed items have neither title nor description',
    'feed_name_already_in_use':
        'feed name "{}" is already in use, please choose a different name',
    'feed_does_not_exist':
        'feed "{}" doesn\'t exist!',
    'fields_of_feed':
        'fields of feed "{}": "{}"',
    'get_help_on_config_keys_with':
        'get help on config keys with: {}rss help config {}',
    'read_hashes_of_feed_from_sqlite_table':
        'read hashes of feed "{}" from sqlite table "{}"',
    'removed_rows_in_table_of_feed':
        'removed {} rows in table "{}" of feed "{}"',
    'saved_config_to_disk':
        'saved config to disk',
    'saved_hash_of_feed_to_sqlite_table':
        'saved hash "{}" of feed "{}" to sqlite table "{}"',
    'synopsis_rss':
        'synopsis: {}rss {}',
    'unable_to_read_feed':
        'unable to read feed',
    'unable_to_read_url_of_feed':
        'unable to read url "{}" of feed "{}"',
    'unable_to_save_config_to_disk':
        'unable to save config to disk!',
    'unable_to_save_hash_of_feed_to_sqlite_table':
        'unable to save hash "{}" of feed "{}" to sqlite table "{}"',
}

FEED_EXAMPLE = '''<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xml:base="http://www.example.com/feed" xmlns:dc="http://purl.org/dc/elements/1.1/">
<channel>
<title>Feed Title</title>
<link>http://www.example.com/feed</link>

<item>
<title>Title</title>
<link>https://github.com/RebelCodeBase/sopel-rss</link>
<description>Description</description>
<summary>Summary</summary>
<author>Author</author>
<pubDate>Sat, 3 Sep 2016 10:00:00 +0000</pubDate>
<guid isPermaLink="false">GUID</guid>
</item>

</channel>
</rss>'''


class RSSSection(StaticSection):
    feeds = ListAttribute('feeds')
    formats = ListAttribute('formats')
    templates = ListAttribute('templates')


def configure(config):
    config.define_section('rss', RSSSection)
    config.rss.configure_setting('feeds', 'comma separated strings consisting of channel, name, url and an optional format separated by pipes')
    config.rss.configure_setting('formats', 'comma separated strings consisting hash and output fields separated by {}'.format(FORMAT_SEPARATOR))
    config.rss.configure_setting('templates', 'comma separated strings consisting format field and template string separated by pipes')


@require_admin(message="Please ask a bot admin for assistance in configuring rss", reply=True)
@commands('rss')
@example(msg='.rss add <channel> <name> <url> [<options>]', user_help=True)
@example(msg='.rss colours', user_help=True)
@example(msg='.rss config <key> [<value>]', user_help=True)
@example(msg='.rss del <name>', user_help=True)
@example(msg='.rss fields <name>', user_help=True)
@example(msg='.rss formats <name> [f=<format>]', user_help=True)
@example(msg='.rss get <name>', user_help=True)
@example(msg='.rss help [<command>]', user_help=True)
@example(msg='.rss list [<feed>|<channel>]', user_help=True)
@example(msg='.rss join', user_help=True)
@example(msg='.rss templates <name> [t=<field1>|<template1>;t=<field1>|<template1>;...]', user_help=True)
@example(msg='.rss update', user_help=True)
def rss(bot, trigger):
    """Command to control the rss plugin. Based off https://github.com/RebelCodeBase/sopel-rss/blob/master/README.md or use .rss help"""
    # trigger(1) == 'rss'
    # trigger(2) are the arguments separated by spaces
    args = shlex.split(trigger.group(2))
    _rss(bot, args)


def setup(bot):
    bot = _config_define(bot)
    _config_read(bot)


def shutdown(bot):
    _config_save(bot)


def _config_concatenate_channels(bot):
    channels = bot.config.core.channels
    for feedname, feed in bot.memory['rss']['feeds'].items():
        if not feed['channel'] in channels:
            channels += [feed['channel']]
    return channels


def _config_concatenate_feeds(bot):
    feeds = []
    for feedname, feed in bot.memory['rss']['feeds'].items():
        newfeed = feed['channel']
        newfeed += CONFIG_SEPARATOR + feed['name']
        newfeed += CONFIG_SEPARATOR + feed['url']

        options = bot.memory['rss']['options'][feedname].get_options()
        if options:
            newfeed += CONFIG_SEPARATOR + options

        feeds.append(newfeed)
        feeds.sort()
    return [','.join(feeds)]


def _config_concatenate_formats(bot):
    formats = list()
    for format in bot.memory['rss']['formats']:

        # only save formats that differ from the default
        if not format == FORMAT_DEFAULT:
            formats.append('f=' + format)
    return [CONFIG_SEPARATOR.join(formats)]


def _config_concatenate_templates(bot):
    templates = list()
    for field in bot.memory['rss']['templates']:
        template = bot.memory['rss']['templates'][field]

        # only save template that differ from the default
        if not TEMPLATES_DEFAULT[field] == template:
            templates.append('t=' + field + '|' + template)
    templates = sorted(templates)
    return [CONFIG_SEPARATOR.join(templates)]


def _config_define(bot):
    bot.config.define_section('rss', RSSSection)
    bot.memory['rss'] = SopelMemory()
    bot.memory['rss']['feeds'] = dict()
    bot.memory['rss']['hashes'] = dict()
    bot.memory['rss']['options'] = dict()
    bot.memory['rss']['formats'] = list()
    bot.memory['rss']['templates'] = dict()
    return bot


def _config_get_feeds(bot):
    bot.say(_config_concatenate_feeds(bot)[0])


def _config_get_formats(bot):
    formats = _config_concatenate_formats(bot)[0]
    if formats:
        formats += CONFIG_SEPARATOR
    formats += 'f=' + FORMAT_DEFAULT
    bot.say(formats)


def _config_get_templates(bot):
    templates = list()
    for field in TEMPLATES_DEFAULT:

        # it's easier to ask forgiveness than it is to get permission
        try:
            template = bot.memory['rss']['templates'][field]
        except KeyError:
            template = TEMPLATES_DEFAULT[field]

        template_string = Options(bot).template_to_irc(template)

        # if the conversion did not work use the default template
        if not template_string:
            template = TEMPLATES_DEFAULT[field]
        templates.append('t=' + field + '|' + template)
    templates = sorted(templates)
    bot.say(CONFIG_SEPARATOR.join(templates))
    bot.say(_config_templates_example(bot))


# read config from disk to memory
def _config_read(bot):

    # read feeds from config file
    if bot.config.rss.feeds and bot.config.rss.feeds[0]:
        _config_split_feeds(bot, bot.config.rss.feeds)

    # read default formats from config file
    if bot.config.rss.formats and bot.config.rss.formats[0]:
        formats = bot.config.rss.formats[0].split(CONFIG_SEPARATOR)
        _config_split_formats(bot, formats)

    # read default templates from config file
    if bot.config.rss.templates and bot.config.rss.templates[0]:
        templates = bot.config.rss.templates[0].split(CONFIG_SEPARATOR)
        _config_split_templates(bot, templates)

    message = 'read config from disk'
    LOGGER.debug(message)


# save config from memory to disk
def _config_save(bot):

    # we want no more than MAX_HASHES in our database
    for feedname in bot.memory['rss']['feeds']:
        _db_remove_old_hashes_from_database(bot, feedname)

    bot.config.core.channels = _config_concatenate_channels(bot)
    bot.config.rss.feeds = _config_concatenate_feeds(bot)
    bot.config.rss.formats = _config_concatenate_formats(bot)
    bot.config.rss.templates = _config_concatenate_templates(bot)

    try:
        bot.config.save()
        message = MESSAGES['saved_config_to_disk']
        LOGGER.debug(message)
    except Exception:
        message = MESSAGES['unable_to_save_config_to_disk']
        LOGGER.error(message)


def _config_set_feeds(bot, value):
    feeds = value.split(',')
    return _config_split_feeds(bot, feeds)


def _config_set_formats(bot, value):
    formats = value.split(CONFIG_SEPARATOR)
    return _config_split_formats(bot, formats)


def _config_set_templates(bot, value):
    templates = value.split(CONFIG_SEPARATOR)
    result = _config_split_templates(bot, templates)
    _config_get_templates(bot)
    return result


def _config_split_feeds(bot, feeds):
    before = len(bot.memory['rss']['feeds'])

    for feed in feeds:

        # split feed by pipes
        atoms = feed.split(CONFIG_SEPARATOR)

        try:
            channel = atoms[0]
            feedname = atoms[1]
            url = atoms[2]
        except IndexError:
            continue

        try:
            options = CONFIG_SEPARATOR.join(atoms[3:])
        except IndexError:
            options = ''

        feedreader = FeedReader(url)
        if _feed_check(bot, feedreader, channel, feedname) == []:
            _feed_add(bot, channel, feedname, url, options)
            _hashes_read(bot, feedname)

    after = len(bot.memory['rss']['feeds'])

    return before != after


def _config_split_formats(bot, formats):
    result = list()

    fields = ''
    for f in TEMPLATES_DEFAULT:
        fields += f

    for format in formats:
        if not format.startswith('f='):
            continue
        format = format[2:]

        # check if format contains only valid fields
        if not set(format) <= set(fields + FORMAT_SEPARATOR):
            continue
        if not Options(bot).is_format_valid(format, FORMAT_SEPARATOR, fields):
            continue
        result.append(format)

    if result:
        bot.memory['rss']['formats'] = result
        return True

    return False


def _config_split_templates(bot, templates):
    result = False

    for f in TEMPLATES_DEFAULT:
        bot.memory['rss']['templates'][f] = TEMPLATES_DEFAULT[f]

    for template in templates:
        if not template.startswith('t='):
            continue
        atoms = template[2:].split('|')
        if len(atoms) == 2:
            if Options(bot).is_template_valid(atoms[1]):
                bot.memory['rss']['templates'][atoms[0]] = atoms[1]
                result = True

    return result


def _config_templates_example(bot):
    feedreader = MockFeedReader(FEED_EXAMPLE)
    options = Options(bot, feedreader, 'f=fl+adfglpsty')
    feed = feedreader.get_feed()
    item = feed['entries'][0]
    return options.get_post('Feedname', item)


def _db_check_if_table_exists(bot, feedname):
    tablename = _digest_tablename(feedname)
    sql_check_table = "SELECT name FROM sqlite_master WHERE type='table' AND name=(?)"
    return bot.db.execute(sql_check_table, (tablename,)).fetchall()


def _db_create_table(bot, feedname):
    tablename = _digest_tablename(feedname)

    # use UNIQUE for column hash to minimize database writes by using
    # INSERT OR IGNORE (which is an abbreviation for INSERT ON CONFLICT IGNORE)
    sql_create_table = "CREATE TABLE '{}' (id INTEGER PRIMARY KEY, hash VARCHAR(32) UNIQUE)".format(tablename)
    bot.db.execute(sql_create_table)
    message = MESSAGES['added_sqlite_table_for_feed'].format(tablename, feedname)
    LOGGER.debug(message)


def _db_drop_table(bot, feedname):
    tablename = _digest_tablename(feedname)
    sql_drop_table = "DROP TABLE '{}'".format(tablename)
    bot.db.execute(sql_drop_table)
    message = MESSAGES['dropped_sqlite_table_of_feed'].format(tablename, feedname)
    LOGGER.debug(message)


def _db_get_number_of_rows(bot, feedname):
    tablename = _digest_tablename(feedname)
    sql_count_hashes = "SELECT count(*) FROM '{}'".format(tablename)
    return bot.db.execute(sql_count_hashes).fetchall()[0][0]


def _db_read_hashes_from_database(bot, feedname):
    tablename = _digest_tablename(feedname)
    sql_hashes = "SELECT * FROM '{}'".format(tablename)
    message = MESSAGES['read_hashes_of_feed_from_sqlite_table'].format(feedname, tablename)
    LOGGER.debug(message)
    return bot.db.execute(sql_hashes).fetchall()


def _db_remove_old_hashes_from_database(bot, feedname):
    tablename = _digest_tablename(feedname)
    rows = _db_get_number_of_rows(bot, feedname)

    if rows > MAX_HASHES_PER_FEED:

        # calculate number of rows to delete in table hashes
        delete_rows = rows - MAX_HASHES_PER_FEED

        # prepare sqlite statement to figure out
        # the ids of those hashes which should be deleted
        sql_first_hashes = "SELECT id FROM '{}' ORDER BY '{}'.id LIMIT (?)".format(tablename, tablename)

        # loop over the hashes which should be deleted
        for row in bot.db.execute(sql_first_hashes, (str(delete_rows),)).fetchall():

            # delete old hashes from database
            sql_delete_hashes = "DELETE FROM '{}' WHERE id = (?)".format(tablename)
            bot.db.execute(sql_delete_hashes, (str(row[0]),))

        message = MESSAGES['removed_rows_in_table_of_feed'].format(str(delete_rows), tablename, feedname)
        LOGGER.debug(message)


def _db_save_hash_to_database(bot, feedname, hash):
    tablename = _digest_tablename(feedname)

    # INSERT OR IGNORE is the short form of INSERT ON CONFLICT IGNORE
    sql_save_hashes = "INSERT OR IGNORE INTO '{}' VALUES (NULL,?)".format(tablename)

    try:
        bot.db.execute(sql_save_hashes, (hash,))
        message = MESSAGES['saved_hash_of_feed_to_sqlite_table'].format(hash, feedname, tablename)
        LOGGER.debug(message)
    except Exception:
        message = MESSAGES['unable_to_save_hash_of_feed_to_sqlite_table'].format(hash, feedname, tablename)
        LOGGER.error(message)


def _digest_tablename(feedname):
    # we need to hash the name of the table as sqlite3 does not permit to parametrize table names
    return 'rss_' + hashlib.md5(feedname.encode('utf-8')).hexdigest()


def _feed_add(bot, channel, feedname, url, options=''):
    # create hash table for this feed in sqlite3 database provided by the sopel framework
    result = _db_check_if_table_exists(bot, feedname)
    if not result:
        _db_create_table(bot, feedname)

    # create new RingBuffer for hashes of feed items
    bot.memory['rss']['hashes'][feedname] = RingBuffer(MAX_HASHES_PER_FEED)
    message = MESSAGES['added_ring_buffer_for_feed'].format(feedname)
    LOGGER.debug(message)

    # create new Options to handle feed hashing and output
    feedreader = FeedReader(url)
    bot.memory['rss']['options'][feedname] = Options(bot, feedreader, options)
    message = MESSAGES['added_feed_formater_for_feed'].format(feedname)
    LOGGER.debug(message)

    # create new dict for feed properties
    bot.memory['rss']['feeds'][feedname] = {'channel': channel, 'name': feedname, 'url': url}

    message_info = MESSAGES['added_rss_feed_to_channel_with_url'].format(feedname, channel, url)
    if options:
        message_info = MESSAGES['added_rss_feed_to_channel_with_url_and_options'].format(feedname, channel, url, options)
    LOGGER.info(message_info)

    return message_info


def _feed_check(bot, feedreader, channel, feedname):
    result = []

    # read feed
    feed = feedreader.get_feed()
    if not feed:
        message = MESSAGES['unable_to_read_feed']
        return [message]

    try:
        item = feed['entries'][0]
    except IndexError:
        message = MESSAGES['unable_to_read_feed']
        return [message]

    # check that feed items have either title or description
    if not hasattr(item, 'title') and not hasattr(item, 'description'):
        message = MESSAGES['feed_items_have_neither_title_nor_description']
        result.append(message)

    # check that feed name is unique
    if _feed_exists(bot, feedname):
        message = MESSAGES['feed_name_already_in_use'].format(feedname)
        result.append(message)

    # check that channel starts with #
    if not channel.startswith('#'):
        message = MESSAGES['channel_must_start_with_a_hash_sign'].format(channel)
        result.append(message)

    return result


def _feed_delete(bot, feedname):
    channel = bot.memory['rss']['feeds'][feedname]['channel']
    url = bot.memory['rss']['feeds'][feedname]['url']

    del(bot.memory['rss']['feeds'][feedname])
    message_info = MESSAGES['deleted_rss_feed_in_channel_with_url'].format(feedname, channel, url)
    LOGGER.info(message_info)

    del(bot.memory['rss']['hashes'][feedname])
    message = MESSAGES['deleted_ring_buffer_for_feed'].format(feedname)
    LOGGER.debug(message)

    _db_drop_table(bot, feedname)
    return message_info


def _feed_exists(bot, feedname):
    if feedname in bot.memory['rss']['feeds']:
        return True
    return False


def _feed_list(bot, feedname):
    feed = bot.memory['rss']['feeds'][feedname]
    feed_options = bot.memory['rss']['options'][feedname].get_options()
    if feed_options:
        bot.say('{} {} {} {}'.format(feed['channel'], feed['name'], feed['url'], feed_options))
    else:
        bot.say('{} {} {}'.format(feed['channel'], feed['name'], feed['url']))


def _feed_templates_example(bot, feedname):
    feedreader = MockFeedReader(FEED_EXAMPLE)
    feedoptions = bot.memory['rss']['options'][feedname].get_options()
    options = Options(bot, feedreader, feedoptions)
    feed = feedreader.get_feed()
    item = feed['entries'][0]
    return options.get_post(feedname, item)


def _feed_update(bot, feedreader, feedname, chatty):
    feed = feedreader.get_feed()

    if not feed:
        url = bot.memory['rss']['feeds'][feedname]['url']
        message = MESSAGES['unable_to_read_url_of_feed'].format(url, feedname)
        LOGGER.error(message)
        return

    channel = bot.memory['rss']['feeds'][feedname]['channel']

    # bot.say new or all items
    for item in reversed(feed['entries']):
        hash = bot.memory['rss']['options'][feedname].get_hash(feedname, item)
        new_item = hash not in bot.memory['rss']['hashes'][feedname].get()
        if chatty or new_item:
            if new_item:
                bot.memory['rss']['hashes'][feedname].append(hash)
                _db_save_hash_to_database(bot, feedname, hash)
            message = bot.memory['rss']['options'][feedname].get_post(feedname, item)
            LOGGER.debug(message)
            bot.say(message, channel)


def _hashes_read(bot, feedname):

    # read hashes from database to memory
    hashes = _db_read_hashes_from_database(bot, feedname)

    # each hash in hashes consists of
    # hash[0]: id
    # hash[1]: md5 hash
    for hash in hashes:
        bot.memory['rss']['hashes'][feedname].append(hash[1])


def _help_config(bot, args):
    args_count = len(args)
    if args_count == 3:
        cmd = args[2]
        _help_text(bot, CONFIG, cmd)
        return

    _help_text(bot, COMMANDS, 'config')
    message = MESSAGES['get_help_on_config_keys_with'].format(bot.config.core.prefix, '|'.join(sorted(CONFIG.keys())))
    bot.say(message)


def _help_text(bot, type, cmd):
    message = type[cmd]['synopsis'].format(bot.config.core.prefix)
    bot.say(message)
    for message in type[cmd]['helptext']:
        bot.say(message)
    message = MESSAGES['examples']
    bot.say(message)
    for message in type[cmd]['examples']:
        bot.say(message.format(bot.config.core.prefix))


def _rss(bot, args):
    args_count = len(args)

    # check if we have a valid command or output general synopsis
    if args_count == 0 or args[0] not in COMMANDS.keys():
        message = MESSAGES['synopsis_rss'].format(
            bot.config.core.prefix, '|'.join(sorted(COMMANDS.keys())))
        bot.say(message)
        return

    cmd = args[0]

    # check if the number of arguments is valid
    present = args_count - 1
    required = COMMANDS[cmd]['required']
    optional = COMMANDS[cmd]['optional']
    if present < required or present > required + optional:
        bot.say(COMMANDS[cmd]['synopsis'].format(bot.config.core.prefix))
        return

    if args_count > 5:
        globals()[COMMANDS['help']['function']](bot, ['help', args[0]])
        return

    # call command function
    globals()[COMMANDS[cmd]['function']](bot, args)


def _rss_add(bot, args):
    channel = args[1]
    feedname = args[2]
    url = args[3]
    options = ''
    if len(args) == 5:
        options = args[4]
    feedreader = FeedReader(url)
    checkresults = _feed_check(bot, feedreader, channel, feedname)
    if checkresults:
        for message in checkresults:
            LOGGER.debug(message)
            bot.say(message)
        return
    message = _feed_add(bot, channel, feedname, url, options)
    bot.say(message)
    bot.join(channel)
    _config_save(bot)


def _rss_colors(bot, args):
    message = ''
    for c in sorted(COLOR):
        message += ESCAPE_COLOR + FOREGROUND[c] + ','
        message += BACKGROUND[c] + ' '
        if int(c) < 16:
            message += c + ': ' + COLOR[c]
        else:
            message += c + ': ' + ESCAPE_CODE[c]
            message += COLOR[c] + ESCAPE_CODE[c]
        message += ' ' + ESCAPE_CODE['20']
    bot.say(message)


def _rss_config(bot, args):
    key = args[1]
    if key not in CONFIG:
        return

    value = ''
    if len(args) == 3:
        value = args[2]

    if not value:
        # call get function
        globals()[CONFIG[key]['func_get']](bot)
        return

    # call set function
    if globals()[CONFIG[key]['func_set']](bot, value):
        _config_save(bot)


def _rss_del(bot, args):
    feedname = args[1]
    if not _feed_exists(bot, feedname):
        message = MESSAGES['feed_does_not_exist'].format(feedname)
        bot.say(message)
        return

    message = _feed_delete(bot, feedname)
    bot.say(message)
    _config_save(bot)


def _rss_fields(bot, args):
    feedname = args[1]
    if not _feed_exists(bot, feedname):
        message = MESSAGES['feed_does_not_exist'].format(feedname)
        bot.say(message)
        return

    fields = bot.memory['rss']['options'][feedname].get_fields()
    message = MESSAGES['fields_of_feed'].format(feedname, fields)
    bot.say(message)


def _rss_formats(bot, args):
    feedname = args[1]

    if not _feed_exists(bot, feedname):
        message = MESSAGES['feed_does_not_exist'].format(feedname)
        bot.say(message)
        return

    if len(args) == 2:
        format = bot.memory['rss']['options'][feedname].get_format()
        message = format
        bot.say(message)
        return

    format = args[2]

    format_before = bot.memory['rss']['options'][feedname].get_format()
    bot.memory['rss']['options'][feedname].set_format(format)
    format_after = bot.memory['rss']['options'][feedname].get_format()

    if not format_before == format_after:
        _config_save(bot)
        message = format_after
        LOGGER.debug(message)
        bot.say(message)
        return

    message = MESSAGES['consider_rss_fields'].format(bot.config.core.prefix, feedname)
    bot.say(message)


def _rss_get(bot, args):
    feedname = args[1]

    if not _feed_exists(bot, feedname):
        message = 'feed "{}" doesn\'t exist!'.format(feedname)
        LOGGER.debug(message)
        bot.say(message)
        return

    url = bot.memory['rss']['feeds'][feedname]['url']
    feedreader = FeedReader(url)
    _feed_update(bot, feedreader, feedname, True)


def _rss_help(bot, args):
    args_count = len(args)

    # check if we have a valid command or output general synopsis
    if args_count == 1 or args[0] not in COMMANDS.keys():
        message = COMMANDS[args[0]]['synopsis'].format(bot.config.core.prefix)
        bot.say(message)
        if args_count == 1:
            message = MESSAGES['command_is_one_of'].format('|'.join(sorted(COMMANDS.keys())))
            bot.say(message)
        return

    # get the command
    cmd = args[1]

    # in case of 'config' we may have to output detailed help on config keys
    if cmd == 'config':
        _help_config(bot, args)
        return

    # output help texts on commands
    _help_text(bot, COMMANDS, cmd)


def _rss_join(bot, args):
    for feedname, feed in bot.memory['rss']['feeds'].items():
        bot.join(feed['channel'])
    if bot.config.core.logging_channel:
        bot.join(bot.config.core.logging_channel)


def _rss_list(bot, args):

    arg = ''
    if len(args) == 2:
        arg = args[1]

    # list feed
    if arg and _feed_exists(bot, arg):
        _feed_list(bot, arg)
        return

    # list feeds in channel
    for feedname, feed in bot.memory['rss']['feeds'].items():
        if arg and arg != feed['channel']:
            continue
        _feed_list(bot, feedname)


def _rss_templates(bot, args):
    feedname = args[1]

    if not _feed_exists(bot, feedname):
        message = MESSAGES['feed_does_not_exist'].format(feedname)
        bot.say(message)
        return

    if len(args) == 2:
        templates = bot.memory['rss']['options'][feedname].get_templates()
        if templates:
            message = templates
            bot.say(message)
            message = _feed_templates_example(bot, feedname)
            bot.say(message)
        return

    templates = args[2]
    templates_before = bot.memory['rss']['options'][feedname].get_templates()
    bot.memory['rss']['options'][feedname].set_templates(templates)
    templates_after = bot.memory['rss']['options'][feedname].get_templates()

    if not templates_before == templates_after:
        _config_save(bot)
        message = templates_after
        LOGGER.debug(message)
        bot.say(message)

    message = _feed_templates_example(bot, feedname)
    bot.say(message)


@interval(UPDATE_INTERVAL)
def _rss_update(bot, args=[]):
    for feedname in bot.memory['rss']['feeds']:

        # the conditional check is necessary to avoid
        # "RuntimeError: dictionary changed size during iteration"
        # which occurs if a feed has been deleted in the meantime
        if _feed_exists(bot, feedname):
            url = bot.memory['rss']['feeds'][feedname]['url']
            feedreader = FeedReader(url)
            _feed_update(bot, feedreader, feedname, False)


# Implementing an rss format handler
class Options:

    LOGGER = get_logger(__name__)

    def __init__(self, bot, feedreader='', options=''):
        self.bot = bot

        if feedreader == '':
            self.feedreader = FeedReader('')
        else:
            self.feedreader = feedreader

        self.separator = FORMAT_SEPARATOR

        self._options_parse(options)

    def get_fields(self):
        return self._format_get_fields(self.feedreader)

    def get_format_default(self):
        for format in self.bot.memory['rss']['formats']:
            return 'f=' + format
        return 'f=' + FORMAT_DEFAULT

    def get_format(self):
        if self.format:
            return 'f=' + self.format
        return self.get_format_default()

    def get_hash(self, feedname, item):
        saneitem = dict()
        saneitem['author'] = self._value_sanitize('author', item)
        saneitem['description'] = self._value_sanitize('description', item)
        saneitem['guid'] = self._value_sanitize('guid', item)
        saneitem['link'] = self._value_sanitize('link', item)
        saneitem['published'] = self._value_sanitize('published', item)
        saneitem['summary'] = self._value_sanitize('summary', item)
        saneitem['title'] = self._value_sanitize('title', item)

        legend = {
            'f': feedname,
            'a': saneitem['author'],
            'd': saneitem['description'],
            'g': saneitem['guid'],
            'l': saneitem['link'],
            'p': saneitem['published'],
            's': saneitem['summary'],
            't': saneitem['title'],
            'y': saneitem['link'],
        }

        signature = ''
        for f in self.get_hashed():
            signature += legend.get(f, '')

        return hashlib.md5(signature.encode('utf-8')).hexdigest()

    def get_hashed(self):
        hashed, output, remainder = self._format_split(self.get_format(), self.separator)
        return hashed

    def get_format_minimal(self):
        fields = self._format_get_fields(self.feedreader)
        if 't' in fields:
            return 'ft+ft'
        return 'fd+fd'

    def get_options(self):
        options = ''
        if self.format:
            options += 'f=' + self.format
        for t in self.templates:
            if options:
                options += CONFIG_SEPARATOR
            options += 't=' + t + TEMPLATE_SEPARATOR + self.templates[t]
        return options

    def get_output(self):
        hashed, output, remainder = self._format_split(self.get_format(), self.separator)
        return output

    def get_post(self, feedname, item):
        saneitem = dict()
        saneitem['author'] = self._value_sanitize('author', item)
        saneitem['description'] = self._value_sanitize('description', item)
        saneitem['guid'] = self._value_sanitize('guid', item)
        saneitem['link'] = self._value_sanitize('link', item)
        saneitem['summary'] = self._value_sanitize('summary', item)
        saneitem['title'] = self._value_sanitize('title', item)

        pubtime = ''
        if 'p' in self.get_output():
            pubtime = time.strftime('%Y-%m-%d %H:%M', item['published_parsed'])
        shorturl = ''
        if 'y' in self.get_output():
            shorturl = self.feedreader.get_tinyurl(saneitem['link'])

        legend = {
            'f': feedname,
            'a': saneitem['author'],
            'd': saneitem['description'],
            'g': saneitem['guid'],
            'l': saneitem['link'],
            'p': pubtime,
            's': saneitem['summary'],
            't': saneitem['title'],
            'y': shorturl,
        }

        templates = self._get_templates_overrides()

        post = ''
        for f in self.get_output():
            post += self.template_to_irc(templates[f]).format(legend.get(f, '')) + ' '

        return post[:-1]

    def get_templates(self):
        templates_list = list()
        for f in sorted(self.templates):
            templates_list.append('t=' + f + TEMPLATE_SEPARATOR + self.templates[f])
        templates = CONFIG_SEPARATOR.join(templates_list)
        return templates

    def is_format_valid(self, format, separator, fields=''):
        hashed, output, remainder = self._format_split(format, separator)
        return(self._is_format_valid(hashed, output, remainder, fields))

    def is_template_valid(self, template):

        # check if template contains exactly one pair of curly brackets
        if template.count('{}') != 1:
            return False

        if not self.template_to_irc(template):
            return False

        return True

    def set_format(self, format_new=''):
        if not format_new.startswith('f='):
            format_new = ''
        else:
            format_new = format_new[2:]
        format_sanitized = self._format_sanitize(format_new)
        if format_new and format_new != format_sanitized:
            return
        self.format = format_sanitized

    def set_format_minimal(self):
        self.format = self.get_format_minimal()

    def set_templates(self, templates):
        templates_split = templates.split(CONFIG_SEPARATOR)
        for template in templates_split:
            if not template.startswith('t='):
                continue
            template = template[2:]
            templates_split = template.split(TEMPLATE_SEPARATOR)
            if not len(templates_split) == 2:
                continue
            f = templates_split[0]
            fields = self._format_get_fields(self.feedreader)
            if f not in fields:
                continue
            t = templates_split[1]
            if not self.is_template_valid(t):
                continue
            self.templates[f] = t

    def template_to_irc(self, template):
        irc = ''
        code = ''
        escape = False
        bgcolor = False

        for character in template:

            # in bgcolor mode?
            if bgcolor and not character == ESCAPE_CHARACTER:
                code += character

                # a background color must start with a dollar sign
                if not code.startswith('$'):

                    # add the next character
                    irc += character
                    code = ''
                    bgcolor = False
                    continue

                # we expect exactly two digits
                if len(code) < 3:
                    continue

                # get the two digits after the comma
                key = code[1:]

                # is it an escape code?
                if key not in ESCAPE_CODE:
                    return ''

                # is it a color?
                # no need to try ... except as all keys are integers
                if not int(key) <= 15:
                    return ''

                # add a background color
                irc += ',' + key
                code = ''
                bgcolor = False
                continue

            # start escape mode?
            if not escape and character == ESCAPE_CHARACTER:
                escape = True
                bgcolor = False
                continue

            # in escape mode?
            if escape:
                code += character

                # escaped escape character handling
                if code == ESCAPE_CHARACTER:
                    irc += ESCAPE_CHARACTER
                    code = ''
                    escape = False
                    continue

                # escaped dollar sign handling
                if code == '$':
                    irc += ','
                    code = ''
                    escape = False
                    continue

                # we expect exactly two digits
                if len(code) < 2:
                    continue

                key = code[:2]

                # check if we have a valid escape sequence
                if key not in ESCAPE_CODE:
                    return ''

                # is it a color code?
                # no need to try ... except as all keys are integers
                if int(key) <= 15:

                    # add the color escape character
                    irc += ESCAPE_COLOR

                    # add a foreground color
                    irc += key

                # not a color code
                else:

                    # add the escape code
                    irc += ESCAPE_CODE[key]

                # end escape mode
                code = ''
                escape = False
                bgcolor = True
                continue

            # add the next character
            irc += character

        # escape mode should be off
        if escape:
            return ''

        return irc

    def _format_get_fields(self, feedreader):
        feed = feedreader.get_feed()

        try:
            item = feed.entries[0]
        except IndexError:
            item = dict()

        fields = 'f'

        if hasattr(item, 'author'):
            fields += 'a'
        if hasattr(item, 'description'):
            fields += 'd'
        if hasattr(item, 'guid'):
            fields += 'g'
        if hasattr(item, 'link'):
            fields += 'l'
        if hasattr(item, 'published') and hasattr(item, 'published_parsed'):
            fields += 'p'
        if hasattr(item, 'summary'):
            fields += 's'
        if hasattr(item, 'title'):
            fields += 't'
        if hasattr(item, 'link'):
            fields += 'y'

        return fields

    def _format_sanitize(self, format):

        # check if format is valid
        if format:
            hashed, output, remainder = self._format_split(format, self.separator)
            if self._is_format_valid(hashed, output, remainder):
                return hashed + self.separator + output

        # check in turn if each default format is valid
        for format in self.bot.memory['rss']['formats']:
            hashed, output, remainder = self._format_split(format, self.separator)
            if self._is_format_valid(hashed, output, remainder):
                return hashed + self.separator + output

        # check if global default format is valid
        hashed, output, remainder = self._format_split(FORMAT_DEFAULT, self.separator)
        if self._is_format_valid(hashed, output, remainder):
            return hashed + self.separator + output

        # else return the minimal valid format
        return self.get_format_minimal()

    def _format_split(self, format, separator):
        format_split = str(format).split(separator)
        hashed = format_split[0]
        try:
            output = format_split[1]
        except IndexError:
            output = ''

        try:
            remainder = format_split[2]
        except IndexError:
            remainder = ''

        return hashed, output, remainder

    def _get_templates_overrides(self):
        templates = dict()

        # use global default templates as basis
        for t in TEMPLATES_DEFAULT:
            templates[t] = TEMPLATES_DEFAULT[t]

        # use custom default templates as overrides
        for t in self.bot.memory['rss']['templates']:
            if self.is_template_valid(self.bot.memory['rss']['templates'][t]):
                templates[t] = self.bot.memory['rss']['templates'][t]

        # use custom feed templates as overrides
        for t in self.templates:
            if self.is_template_valid(self.templates[t]):
                templates[t] = self.templates[t]

        return templates

    def _is_format_valid(self, hashed, output, remainder, fields=''):

        # check format for duplicate separators
        if remainder:
            return False

        # check if hashed is empty
        if not len(hashed):
            return False

        # check if output is empty
        if not len(output):
            return False

        # check if hashed contains only the feedname
        if hashed == 'f':
            return False

        # check if hashed contains only the feedname
        if output == 'f':
            return False

        if not fields:
            fields = self._format_get_fields(self.feedreader)

        # check hashed has only valid fields
        for f in hashed:
            if f not in fields:
                return False

        # check output has only valid fields
        for f in output:
            if f not in fields:
                return False

        # check hashed for duplicates
        if len(hashed) > len(set(hashed)):
            return False

        # check output for duplicates
        if len(output) > len(set(output)):
            return False

        return True

    def _options_parse(self, options):
        self.format = ''
        self.templates = dict()

        if not options:
            return

        options_split = options.split(CONFIG_SEPARATOR)

        for option in options_split:
            if option.startswith('f='):
                self.set_format_minimal()
                self.set_format(option)
            elif option.startswith('t='):
                self.set_templates(option)

    def _value_sanitize(self, key, item):
        if hasattr(item, key):
            return item[key]
        return ''


# Implementing an rss feed reader for dependency injection
class FeedReader:
    def __init__(self, url):
        self.url = url

    def get_feed(self):
        try:
            feed = feedparser.parse(self.url)
            return feed
        except Exception:
            return dict()

    def get_tinyurl(self, url):
        tinyurlapi = 'https://tinyurl.com/api-create.php'
        data = urllib.parse.urlencode({'url': url}).encode("utf-8")
        req = urllib.request.Request(tinyurlapi, data)
        tinyurl = urllib.request.urlopen(req).read().decode('utf-8')
        if tinyurl.startswith('http'):
            return tinyurl
        return url


# Implementing a mock rss feed reader
class MockFeedReader:
    def __init__(self, url):
        self.url = url

    def get_feed(self):
        try:
            feed = feedparser.parse(self.url)
            return feed
        except Exception:
            return dict()

    def get_tinyurl(self, url):
        return 'https://tinyurl.com/govvpmm'


# Implementing a ring buffer
# https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch05s19.html
class RingBuffer:
    """ class that implements a not-yet-full buffer """

    def __init__(self, size_max):
        self.max = size_max
        self.index = 0
        self.data = []

    class __Full:
        """ class that implements a full buffer """

        def append(self, x):
            """ Append an element overwriting the oldest one. """
            self.data[self.cur] = x
            self.cur = (self.cur + 1) % self.max

        def get(self):
            """ return list of elements in correct order """
            return self.data[self.cur:] + self.data[:self.cur]

    def append(self, x):
        """ append an element at the end of the buffer """
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            # Permanently change self's class from non-full to full
            self.__class__ = self.__Full

    def get(self):
        """ return a list of elements from the oldest to the newest. """
        return self.data
