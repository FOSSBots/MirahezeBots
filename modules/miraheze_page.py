# coding=utf-8
# Copyright 2013 Elsie Powell - embolalia.com
# Licensed under the Eiffel Forum License 2.
from __future__ import unicode_literals, absolute_import, print_function, division
from sopel import web, tools
from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import NOLIMIT, commands, example, rule
import json
import re

import sys
if sys.version_info.major < 3:
    from urlparse import unquote as _unquote
    unquote = lambda s: _unquote(s.encode('utf-8')).decode('utf-8')
else:
    from urllib.parse import unquote

REDIRECT = re.compile(r'^REDIRECT (.*)')


class MirahezeSection(StaticSection):
    default_lang = ValidatedAttribute('default_lang', default='meta')
    """The default language to find articles from."""
    lang_per_channel = ValidatedAttribute('lang_per_channel')


def setup(bot):
    bot.config.define_section('miraheze_page', MirahezeSection)

    regex = re.compile('([a-z]+).(meta.miraheze.org/wiki/)([^ ]+)')
    if not bot.memory.contains('url_callbacks'):
        bot.memory['url_callbacks'] = tools.SopelMemory()
    bot.memory['url_callbacks'][regex] = mw_info


def configure(config):
    config.define_section('miraheze_page', MirahezeSection)
    config.wikipedia.configure_setting(
        'meta',
        "Enter the default language to find articles from."
    )


def mw_search(server, query, num):
    """
    Searches the specified MediaWiki server for the given query, and returns
    the specified number of results.
    """
    search_url = ('https://%s/w/api.php?format=json&action=query'
                  '&list=search&srlimit=%d&srprop=timestamp&srwhat=text'
                  '&srsearch=') % (server, num)
    search_url += query
    query = json.loads(web.get(search_url))
    if 'query' in query:
        query = query['query']['search']
        return [r['title'] for r in query]
    else:
        return None


def say_snippet(bot, server, query, show_url=True):
    page_name = query.replace('_', ' ')
    query = query.replace(' ', '_')
    snippet = mw_snippet(server, query)
    msg = '[MIRAHEZE META] {} | "{}"'.format(page_name, snippet)
    if show_url:
        msg = msg + ' | https://{}/wiki/{}'.format(server, query)
    bot.say(msg)


def mw_snippet(server, query):
    """
    Retrives a snippet of the specified length from the given page on the given
    server.
    """
    snippet_url = ('https://' + server + '/w/api.php?format=json'
                   '&action=query&prop=extracts&exintro&explaintext'
                   '&exchars=300&redirects&titles=')
    snippet_url += query
    snippet = json.loads(web.get(snippet_url))
    snippet = snippet['query']['pages']

    # For some reason, the API gives the page *number* as the key, so we just
    # grab the first page number in the results.
    snippet = snippet[list(snippet.keys())[0]]

    return snippet['extract']


@rule('.*/(meta.miraheze.org)/wiki/([^ ]+).*')
def mw_info(bot, trigger, found_match=None):
    """
    Retrives a snippet of the specified length from the given page on the given
    server.
    """
    match = found_match or trigger
    say_snippet(bot, match.group(1), unquote(match.group(2)), show_url=False)


@commands('mh', 'miraheze_page', 'mhw')
@example('.mh Miraheze')
def wikipedia(bot, trigger):
    lang = 'meta'

    if trigger.group(2) is None:
        bot.reply("What do you want me to look up?")
        return NOLIMIT
    
    query = trigger.group(2)
    args = re.search(r'^-([a-z]{2,12})\s(.*)', query)
    if args is not None:
        lang = args.group(1)
        query = args.group(2)

    if not query:
        bot.reply('What do you want me to look up?')
        return NOLIMIT
    server = lang + '.miraheze.org'
    query = mw_search(server, query, 1)
    if not query:
        bot.reply("I can't find any results for that.")
        return NOLIMIT
    else:
        query = query[0]
    say_snippet(bot, server, query)

