# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import MirahezeBots.plugins.rss as rss
from sopel.tools import SopelMemory
from sopel.tests import rawlist
# from sopel.db import SopelDB
import hashlib
import pytest

FEED_VALID = '''<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xml:base="https://www.site1.com/feed" xmlns:dc="https://purl.org/dc/elements/1.1/">
<channel>
<title>Site 1 Articles</title>
<link>https://www.site1.com/feed</link>
<description></description>
<language>en</language>
<item>
<title>Title 3</title>
<link>https://www.site1.com/article3</link>
<description>Description of article 3</description>
<summary>Summary of article 3</summary>
<author>Author 3</author>
<pubDate>Sat, 23 Aug 2016 03:30:33 +0000</pubDate>
<guid isPermaLink="false">3 at https://www.site1.com/</guid>
</item>
<item>
<title>Title 2</title>
<link>https://www.site1.com/article2</link>
<description>Description of article 2</description>
<summary>Summary of article 2</summary>
<author>Author 2</author>
<pubDate>Sat, 22 Aug 2016 02:20:22 +0000</pubDate>
<guid isPermaLink="false">2 at https://www.site1.com/</guid>
</item>
<item>
<title>Title 1</title>
<link>https://www.site1.com/article1</link>
<description>Description of article 1</description>
<summary>Summary of article 1</summary>
<author>Author 1</author>
<pubDate>Sat, 21 Aug 2016 01:10:11 +0000</pubDate>
<guid isPermaLink="false">1 at https://www.site1.com/</guid>
</item>
</channel>
</rss>'''


FEED_BASIC = '''<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xml:base="https://www.site1.com/feed" xmlns:dc="https://purl.org/dc/elements/1.1/">
<channel>
<title>Site 1 Articles</title>
<link>https://www.site1.com/feed</link>
<item>
<title>Title 3</title>
<link>https://www.site1.com/article3</link>
</item>
<item>
<title>Title 2</title>
<link>https://www.site1.com/article2</link>
</item>
<item>
<title>Title 1</title>
<link>https://www.site1.com/article1</link>
</item>
</channel>
</rss>'''


FEED_INVALID = '''<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xml:base="https://www.site1.com/feed" xmlns:dc="https://purl.org/dc/elements/1.1/">
<channel>
<title>Site 1 Articles</title>
<link>https://www.site1.com/feed</link>
<description></description>
<language>en</language>
</channel>
</rss>'''


FEED_ITEM_NEITHER_TITLE_NOR_DESCRIPTION = '''<?xml version="1.0" encoding="utf-8" ?>
<rss version="2.0" xml:base="https://www.site1.com/feed" xmlns:dc="https://purl.org/dc/elements/1.1/">
<channel>
<title>Site</title>
<link>https://www.site.com/feed</link>
<description></description>
<item>
<link>https://www.site.com/article</link>
</item>
</channel>
</rss>'''


FEED_SPY = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
 <title>News About <![CDATA[S&P Depository Receipts]]></title>
 <link><![CDATA[https://markets.financialcontent.com/stocks/action/rssfeed]]></link>
 <description>News About <![CDATA[S&P Depository Receipts]]></description>
 <language>en-us</language>
 <item>
  <title><![CDATA[Deutsche Bank Predicts 10% Pullback in S&P 500]]></title>
  <link><![CDATA[https://markets.financialcontent.com/stocks/news/read?GUID=32821698&Symbol=SPY]]></link>
  <pubDate><![CDATA[Sun, 11 Sep 2016 07:37:24 -0400]]></pubDate>
  <guid><![CDATA[https://markets.financialcontent.com/stocks/news/read?GUID=32821698&Symbol=SPY]]></guid>
 </item>
</channel>
</rss>
'''

TMP_CONFIG = """
[core]
owner = testnick
nick = TestBot
enable = coretasks, rss
"""


@pytest.fixture
def tmpconfig(configfactory):
    return configfactory('test.cfg', TMP_CONFIG)


@pytest.fixture
def mockbot(tmpconfig, botfactory):
    mockbot = botfactory.preloaded(tmpconfig, preloads=['rss'])
    mockbot.memory['rss'] = SopelMemory()
    mockbot.memory['rss']['feeds'] = dict()
    mockbot.memory['rss']['hashes'] = dict()
    mockbot.memory['rss']['options'] = dict()
    mockbot.memory['rss']['formats'] = list()
    mockbot.memory['rss']['templates'] = dict()
    # mockbot.db = SopelDB(mockbot)
    return mockbot


def _fixture_bot_add_data(mockbot, id, url):
    mockbot.memory['rss']['feeds']['feed' + id] = {'channel': '#channel' + id, 'name': 'feed' + id, 'url': url}
    mockbot.memory['rss']['hashes']['feed' + id] = rss.RingBuffer(100)
    feedreader = rss.MockFeedReader(FEED_VALID)
    mockbot.memory['rss']['options']['feed' + id] = rss.Options(mockbot, feedreader)
    # sql_create_table = 'CREATE TABLE ' + rss._digest_tablename('feed' + id) + ' (id INTEGER PRIMARY KEY, hash VARCHAR(32) UNIQUE)'
    # bot.db.execute(sql_create_table)
    # bot.config.core.channels = ['#channel' + id]
    return mockbot


@pytest.fixture(scope="function")
def bot(request, mockbot):
    bot = _fixture_bot_add_data(mockbot, '1', 'https://www.site1.com/feed')
    return bot


@pytest.fixture(scope="function")
def bot_config_save(request, mockbot):
    bot = _fixture_bot_add_data(mockbot, '1', 'https://www.site1.com/feed')
    return bot


@pytest.fixture(scope="function")
def mockbot_rss_list(request, mockbot):
    bot = _fixture_bot_add_data(mockbot, '1', 'https://www.site1.com/feed')
    bot = _fixture_bot_add_data(mockbot, '2', 'https://www.site2.com/feed')
    return bot


@pytest.fixture(scope="function")
def mockbot_rss_update(request, mockbot):
    bot = _fixture_bot_add_data(mockbot, '1', FEED_VALID)
    return bot


@pytest.fixture(scope="module")
def feedreader_feed_valid():
    return rss.MockFeedReader(FEED_VALID)


@pytest.fixture(scope="module")
def feedreader_feed_invalid():
    return rss.MockFeedReader(FEED_INVALID)


@pytest.fixture(scope="module")
def feedreader_feed_item_neither_title_nor_description():
    return rss.MockFeedReader(FEED_ITEM_NEITHER_TITLE_NOR_DESCRIPTION)

def make_wrapper_mock(mockbot, triggerfactory, line):
    wrapper = triggerfactory.wrapper(mockbot, line)
    return wrapper


def test_rss_global_too_many_parameters(mockbot, triggerfactory):
    wrapper = make_wrapper_mock(mockbot, triggerfactory, "PRIVMSG #channel .rss add #channel feedname {} f=fl+ftl fifth_argument".format(FEED_VALID))
    rss._rss(wrapper, ['add', '#channel', 'feedname', FEED_VALID, 'f=fl+ftl', 'fifth_argument'])
    expected = rawlist("PRIVMSG #channel :" + rss.COMMANDS['add']['synopsis'].format(mockbot.config.core.prefix))
    assert expected == wrapper.backend.message_sent


def test_rss_global_too_few_parameters(mockbot):
    rss._rss(mockbot, ['add', '#channel', 'feedname'])
    expected = rss.COMMANDS['add']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    assert expected == bot.output


def test_rss_global_color(mockbot):
    rss._rss(mockbot, ['colors'])
    expected = '\x0301,00 00: white \x0f\x0300,01 01: black \x0f\x0300,02 02: blue \x0f\x0300,03 03: green \x0f\x0301,04 04: red \x0f\x0300,05 05: brown \x0f\x0300,06 06: purple \x0f\x0301,07 07: orange \x0f\x0301,08 08: yellow \x0f\x0301,09 09: lime \x0f\x0300,10 10: cyan \x0f\x0301,11 11: aqua \x0f\x0301,12 12: azure \x0f\x0301,13 13: pink \x0f\x0300,14 14: grey \x0f\x0301,15 15: silver \x0f\x0300,01 16: \x02bold\x02 \x0f\x0301,00 17: \x1ditalic\x1d \x0f\x0300,01 18: \x1funderline\x1f \x0f\n'   # noqa: E501
    assert expected == bot.output


def test_rss_global_config_templates(mockbot):
    rss._rss(mockbot, ['config', 'templates'])
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|{};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_global_feed_add(mockbot):
    rss._rss(mockbot, ['add', '#channel', 'feedname', FEED_VALID])
    assert rss._feed_exists(mockbot, 'feedname')


def test_rss_global_feed_delete(mockbot):
    rss._rss(mockbot, ['add', '#channel', 'feedname', FEED_VALID])
    rss._rss(mockbot, ['del', 'feedname'])
    assert rss._feed_exists(mockbot, 'feedname') is False


def test_rss_global_fields_get(mockbot):
    rss._rss(mockbot, ['fields', 'feed1'])
    expected = rss.MESSAGES['fields_of_feed'].format('feed1', 'fadglpsty') + '\n'
    assert expected == bot.output


def test_rss_global_formats_set(mockbot):
    rss._rss(mockbot, ['formats', 'feed1', 'f=asl+als'])
    format_new = bot.memory['rss']['options']['feed1'].get_format()
    assert 'f=asl+als' == format_new


def test_rss_global_formats_feed(mockbot):
    rss._rss(mockbot, ['formats', 'feed1', 'f=apl+atl'])
    bot.output = ''
    args = ['config', 'feeds']
    rss._rss_config(mockbot, args)
    expected = '#channel1' + rss.CONFIG_SEPARATOR + 'feed1' + rss.CONFIG_SEPARATOR + 'https://www.site1.com/feed' + rss.CONFIG_SEPARATOR + 'f=apl+atl\n'
    assert expected == bot.output


def test_rss_global_get_post_feed_items(mockbot):
    rss._rss(mockbot, ['add', '#channel', 'feedname', FEED_VALID])
    bot.output = ''
    rss._rss(mockbot, ['get', 'feedname'])
    expected = '\x02[feedname]\x02 Title 1 \x02→\x02 https://www.site1.com/article1\n\x02[feedname]\x02 Title 2 \x02→\x02 https://www.site1.com/article2\n\x02[feedname]\x02 Title 3 \x02→\x02 https://www.site1.com/article3\n'  # noqa: E501
    assert expected == bot.output


def test_rss_global_help_synopsis_help(mockbot):
    rss._rss(mockbot, ['help'])
    expected = rss.COMMANDS['help']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    expected += rss.MESSAGES['command_is_one_of'].format('|'.join(sorted(rss.COMMANDS.keys()))) + '\n'
    assert expected == bot.output


def test_rss_global_join(mockbot):
    rss._rss(mockbot, ['join'])
    channels = []
    for feed in bot.memory['rss']['feeds']:
        feedchannel = bot.memory['rss']['feeds'][feed]['channel']
        if feedchannel not in channels:
            channels.append(feedchannel)
    assert channels == bot.config.core.channels


def test_rss_global_list_feed(mockbot):
    rss._rss(mockbot, ['list', 'feed1'])
    expected = '#channel1 feed1 https://www.site1.com/feed\n'
    assert expected == bot.output


def test_rss_global_list_feed_options(mockbot):
    rss._rss(mockbot, ['add', '#channel', 'feed', FEED_VALID])
    rss._rss(mockbot, ['formats', 'feed', 'f=l+tl'])
    rss._rss(mockbot, ['templates', 'feed', 't=t|%06[{}]%20'])
    bot.output = ''
    rss._rss(mockbot, ['list', 'feed'])
    expected = '#channel feed ' + FEED_VALID + ' f=l+tl;t=t|%06[{}]%20\n'
    assert expected == bot.output


def test_rss_global_templates_get(mockbot):
    rss._rss(mockbot, ['templates', 'feed1'])
    assert '' == bot.output


def test_rss_global_update_update(mockbot_rss_update):
    rss._rss(mockbot_rss_update, ['update'])
    expected = '\x02[feed1]\x02 Title 1 \x02→\x02 https://www.site1.com/article1\n\x02[feed1]\x02 Title 2 \x02→\x02 https://www.site1.com/article2\n\x02[feed1]\x02 Title 3 \x02→\x02 https://www.site1.com/article3\n'
    assert expected == mockbot_rss_update.output


# def test_config_define_sopelmemory():
    # bot = MockSopel('Sopel')
    # bot = rss._config_define(mockbot)
    # assert isinstance(mockbot.memory['rss'], rss.SopelMemory)


# def test_config_define_feeds():
    # bot = MockSopel('Sopel')
    # bot = rss._config_define(mockbot)
    # assert isinstance(mockbot.memory['rss']['feeds'], dict)


# def test_config_define_hashes():
    # bot = MockSopel('Sopel')
    # bot = rss._config_define(mockbot)
    # assert isinstance(mockbot.memory['rss']['hashes'], dict)


# def test_config_define_formats():
    # bot = MockSopel('Sopel')
    # bot = rss._config_define(mockbot)
    # assert isinstance(mockbot.memory['rss']['options'], dict)


def test_config_concatenate_channels(mockbot):
    channels = rss._config_concatenate_channels(mockbot)
    expected = ['#channel1']
    assert expected == channels


def test_config_concatenate_feeds(mockbot, feedreader_feed_valid):
    bot.memory['rss']['options']['feed1'] = rss.Options(mockbot, feedreader_feed_valid, 'f=fy+fty')
    feeds = rss._config_concatenate_feeds(mockbot)
    expected = ['#channel1' + rss.CONFIG_SEPARATOR + 'feed1' + rss.CONFIG_SEPARATOR + 'https://www.site1.com/feed' + rss.CONFIG_SEPARATOR + 'f=fy+fty']
    assert expected == feeds


def test_config_concatenate_formats(mockbot):
    bot.memory['rss']['formats'] = ['yt+yt', 'ftla+ft']
    formats = rss._config_concatenate_formats(mockbot)
    expected = ['f=yt+yt;f=ftla+ft']
    assert expected == formats


def test_config_concatenate_templates(mockbot):
    bot.memory['rss']['templates']['t'] = '<>t<>'
    templates = rss._config_concatenate_templates(mockbot)
    expected = ['t=t|<>t<>']
    assert expected == templates


def test_config_read_feed_default(mockbot):
    rss._config_read(mockbot)
    feeds = mockbot.memory['rss']['feeds']
    expected = {}
    assert expected == feeds


def test_config_read_format_default(mockbot):
    mockbot.config.rss.formats = ['f=' + rss.FORMAT_DEFAULT]
    rss._config_read(mockbot)
    formats = mockbot.memory['rss']['formats']
    expected = [rss.FORMAT_DEFAULT]
    assert expected == formats


def test_config_read_format_custom_valid(mockbot):
    formats_custom = ['f=al+fpatl;f=y+fty']
    mockbot.config.rss.formats = formats_custom
    rss._config_read(mockbot)
    formats = mockbot.memory['rss']['formats']
    expected = ['al+fpatl', 'y+fty']
    assert expected == formats


def test_config_read_format_custom_invalid(mockbot):
    formats_custom = ['f=al+fpatl;f=yy+fty']
    mockbot.config.rss.formats = formats_custom
    rss._config_read(mockbot)
    formats = mockbot.memory['rss']['formats']
    expected = ['al+fpatl']
    assert expected == formats


def test_config_read_template_default(mockbot):
    for t in rss.TEMPLATES_DEFAULT:
        mockbot.config.rss.templates.append('t=' + t + '|' + rss.TEMPLATES_DEFAULT[t])
    rss._config_read(mockbot)
    templates = mockbot.memory['rss']['templates']
    expected = rss.TEMPLATES_DEFAULT
    assert expected == templates


def test_config_read_template_custom(mockbot):
    templates_custom = ['t=t|>>{}<<']
    mockbot.config.rss.templates = templates_custom
    rss._config_read(mockbot)
    templates = mockbot.memory['rss']['templates']
    expected = dict()
    for t in rss.TEMPLATES_DEFAULT:
        expected[t] = rss.TEMPLATES_DEFAULT[t]
    expected['t'] = '>>{}<<'
    assert expected == templates


def FIXME_test_config_save_writes(mockbot_config_save):
    bot_config_save.memory['rss']['options']['feed1'].set_format('f=fl+ftl')
    bot_config_save.memory['rss']['options']['feed1'].set_templates('t=t|>>{}<<')
    bot_config_save.memory['rss']['formats'] = ['ft+ftpal']
    for t in rss.TEMPLATES_DEFAULT:
        bot_config_save.memory['rss']['templates'][t] = rss.TEMPLATES_DEFAULT[t]
    bot_config_save.memory['rss']['templates']['t'] = '<<{}>>'
    rss._config_save(mockbot_config_save)
    expected = '''[core]
owner = ''' + '''
admins = ''' + '''
homedir = ''' + bot_config_save.config.homedir + '''
db_filename = ''' + bot_config_save.db.filename + '''
channels = #channel1
[rss]
feeds = #channel1''' + rss.CONFIG_SEPARATOR + '''feed1''' + rss.CONFIG_SEPARATOR + '''https://www.site1.com/feed''' + rss.CONFIG_SEPARATOR + '''f=fl+ftl;t=t|>>{}<<
formats = f=ft+ftpal
templates = t=t|<<{}>>
'''
    f = open(mockbot_config_save.config.filename, 'r')
    config = f.read()
    assert expected == config


def test_config_set_feeds_change_returns_true(mockbot):
    feeds = '#channel' + rss.CONFIG_SEPARATOR + 'feed' + rss.CONFIG_SEPARATOR + FEED_BASIC + rss.CONFIG_SEPARATOR + 'f=fl+ftl'
    result = rss._config_set_feeds(mockbot, feeds)
    assert result is True


def test_config_set_feeds_no_change_returns_false(mockbot):
    feeds = ''
    result = rss._config_set_feeds(mockbot, feeds)
    assert result is False


def test_config_set_feeds_get(mockbot):
    feeds = '#channelA' + rss.CONFIG_SEPARATOR + 'feedA' + rss.CONFIG_SEPARATOR + FEED_BASIC + rss.CONFIG_SEPARATOR + \
        'f=t+t,#channelB' + rss.CONFIG_SEPARATOR + 'feedB' + rss.CONFIG_SEPARATOR + FEED_BASIC + rss.CONFIG_SEPARATOR + 'f=tl+tl'
    rss._config_set_feeds(mockbot, feeds)
    rss._config_get_feeds(mockbot)
    expected = feeds + '\n'
    assert expected == mockbot.output


def test_config_set_feeds_exists(mockbot):
    feeds = '#channelA' + rss.CONFIG_SEPARATOR + 'feedA' + rss.CONFIG_SEPARATOR + FEED_BASIC + rss.CONFIG_SEPARATOR + \
        'f=fyg+fgty,#channelB' + rss.CONFIG_SEPARATOR + 'feedB' + rss.CONFIG_SEPARATOR + FEED_BASIC + rss.CONFIG_SEPARATOR + 'f=lp+fptl'
    rss._config_set_feeds(mockbot, feeds)
    result = rss._feed_exists(mockbot, 'feedB')
    assert result is True


def test_config_set_formats_change_returns_true(mockbot):
    formats = 'f=t+t'
    result = rss._config_set_formats(mockbot, formats)
    assert result is True


def test_config_set_formats_no_change_returns_false(mockbot):
    formats = ''
    result = rss._config_set_formats(mockbot, formats)
    assert result is False


def test_config_set_formats_get(mockbot):
    formats = 'f=t+t;f=d+d'
    rss._config_set_formats(mockbot, formats)
    rss._config_get_formats(mockbot)
    expected = formats + ';f=' + rss.FORMAT_DEFAULT + '\n'
    assert expected == bot.output


def test_config_set_formats_join(mockbot):
    formats = 'f=t+t;f=d+d'
    rss._config_set_formats(mockbot, formats)
    formats_bot = ''
    for format in bot.memory['rss']['formats']:
        formats_bot += 'f=' + format + ';'
    assert formats == formats_bot[:-1]


def test_config_set_templates_change_returns_true(mockbot):
    templates = 't=t|≈{}≈'
    result = rss._config_set_templates(mockbot, templates)
    assert result is True


def test_config_set_templates_no_change_returns_false(mockbot):
    templates = ''
    result = rss._config_set_templates(mockbot, templates)
    assert result is False


def test_config_set_templates_get(mockbot):
    templates = 't=t|≈{}≈;t=s|√{}'
    rss._config_set_templates(mockbot, templates)
    bot.output = ''
    rss._config_get_templates(mockbot)
    expected_dict = dict()
    for t in rss.TEMPLATES_DEFAULT:
        expected_dict[t] = rss.TEMPLATES_DEFAULT[t]
    expected_dict['s'] = '√{}'
    expected_dict['t'] = '≈{}≈'
    expected_list = list()
    for t in expected_dict:
        expected_list.append('t=' + t + '|' + expected_dict[t])
    expected = ';'.join(sorted(expected_list)) + '\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_config_set_templates_dict(mockbot):
    templates = 't=t|≈{}≈;t=s|√{}'
    rss._config_set_templates(mockbot, templates)
    template = bot.memory['rss']['templates']['s']
    assert '√{}' == template


def test_config_split_feeds_valid(mockbot):
    feeds = ['#channel2' + rss.CONFIG_SEPARATOR + 'feed2' + rss.CONFIG_SEPARATOR + FEED_VALID + rss.CONFIG_SEPARATOR + 'f=fy+fty']
    rss._config_split_feeds(mockbot, feeds)
    result = rss._feed_exists(mockbot, 'feed2')
    assert result is True


def test_config_split_feeds_invalid(mockbot):
    feeds = ['#channel2' + rss.CONFIG_SEPARATOR + 'feed2' + rss.CONFIG_SEPARATOR + FEED_INVALID + rss.CONFIG_SEPARATOR + 'f=fy+fty']
    rss._config_split_feeds(mockbot, feeds)
    result = rss._feed_exists(mockbot, 'feed2')
    assert result is False


def test_config_split_feeds_format_and_template(mockbot):
    feeds = ['#channel2' + rss.CONFIG_SEPARATOR + 'feed2' + rss.CONFIG_SEPARATOR + FEED_VALID + rss.CONFIG_SEPARATOR + 'f=fy+fty;t=t|+++{}+++']
    rss._config_split_feeds(mockbot, feeds)
    result = rss._feed_exists(mockbot, 'feed2')
    assert result is True


def test_config_split_formats_valid(mockbot):
    formats = ['f=yt+yt', 'f=ftla+ft']
    rss._config_split_formats(mockbot, formats)
    formats_split = bot.memory['rss']['formats']
    expected = ['yt+yt', 'ftla+ft']
    assert expected == formats_split


def test_config_split_formats_invalid(mockbot):
    formats = ['f=abcd', 'f=ftla+ft']
    rss._config_split_formats(mockbot, formats)
    formats_split = bot.memory['rss']['formats']
    expected = ['ftla+ft']
    assert expected == formats_split


def test_config_split_templates_valid(mockbot):
    templates = {'t=t|>>{}<<'}
    rss._config_split_templates(mockbot, templates)
    templates_split = bot.memory['rss']['templates']
    assert templates_split['t'] == '>>{}<<'


def test_config_split_templates_invalid(mockbot):
    templates = {'t=t|>><<'}
    rss._config_split_templates(mockbot, templates)
    templates_split = bot.memory['rss']['templates']
    assert templates_split['t'] == '{}'


def test_db_create_table_and_db_check_if_table_exists(mockbot):
    rss._db_create_table(mockbot, 'feedname')
    result = rss._db_check_if_table_exists(mockbot, 'feedname')
    assert [(rss._digest_tablename('feedname'),)] == result


def test_db_drop_table(mockbot):
    rss._db_create_table(mockbot, 'feedname')
    rss._db_drop_table(mockbot, 'feedname')
    result = rss._db_check_if_table_exists(mockbot, 'feedname')
    assert [] == result


def test_config_templates_example(mockbot):
    example = rss._config_templates_example(mockbot)
    expected = '<Author> Description \x02[Feedname]\x02 GUID \x02→\x02 https://github.com/RebelCodeBase/sopel-rss (2016-09-03 10:00) Description Title \x02→\x02 https://tinyurl.com/govvpmm'
    assert expected == example


def test_db_get_numer_of_rows(mockbot):
    ROWS = 10
    for i in range(ROWS):
        hash = rss.hashlib.md5(str(i).encode('utf-8')).hexdigest()
        bot.memory['rss']['hashes']['feed1'].append(hash)
        rss._db_save_hash_to_database(mockbot, 'feed1', hash)
    rows_feed = rss._db_get_number_of_rows(mockbot, 'feed1')
    assert ROWS == rows_feed


def test_db_remove_old_hashes_from_database(mockbot):
    SURPLUS_ROWS = 10
    bot.memory['rss']['hashes']['feed1'] = rss.RingBuffer(rss.MAX_HASHES_PER_FEED + SURPLUS_ROWS)
    for i in range(rss.MAX_HASHES_PER_FEED + SURPLUS_ROWS):
        hash = hashlib.md5(str(i).encode('utf-8')).hexdigest()
        bot.memory['rss']['hashes']['feed1'].append(hash)
        rss._db_save_hash_to_database(mockbot, 'feed1', hash)
    rss._db_remove_old_hashes_from_database(mockbot, 'feed1')
    rows_feed = rss._db_get_number_of_rows(mockbot, 'feed1')
    assert rss.MAX_HASHES_PER_FEED == rows_feed


def test_db_save_hash_to_database(mockbot):
    rss._db_save_hash_to_database(mockbot, 'feed1', '463f9357db6c20a94a68f9c9ef3bb0fb')
    hashes = rss._db_read_hashes_from_database(mockbot, 'feed1')
    expected = [(1, '463f9357db6c20a94a68f9c9ef3bb0fb')]
    assert expected == hashes


def test_digest_tablename_works():
    digest = rss._digest_tablename('thisisatest')
    assert 'rss_f830f69d23b8224b512a0dc2f5aec974' == digest


def test_feed_add_create_db_table(mockbot):
    rss._feed_add(mockbot, '#channel', 'feedname', FEED_VALID)
    result = rss._db_check_if_table_exists(mockbot, 'feedname')
    assert [(rss._digest_tablename('feedname'),)] == result


def test_feed_add_create_ring_buffer(mockbot):
    rss._feed_add(mockbot, '#channel', 'feedname', FEED_VALID)
    assert isinstance(mockbot.memory['rss']['hashes']['feedname'], rss.RingBuffer)


def test_feed_add_create_feed(mockbot):
    rss._feed_add(mockbot, '#channel', 'feedname', FEED_VALID)
    feed = bot.memory['rss']['feeds']['feedname']
    assert {'name': 'feedname', 'url': FEED_VALID, 'channel': '#channel'} == feed


def test_feed_check_feed_valid(mockbot, feedreader_feed_valid):
    checkresults = rss._feed_check(mockbot, feedreader_feed_valid, '#newchannel', 'newname')
    assert not checkresults


def test_feed_check_feedname_must_be_unique(mockbot, feedreader_feed_valid):
    checkresults = rss._feed_check(mockbot, feedreader_feed_valid, '#newchannel', 'feed1')
    expected = [rss.MESSAGES['feed_name_already_in_use'].format('feed1')]
    assert expected == checkresults


def test_feed_check_channel_must_start_with_hash(mockbot, feedreader_feed_valid):
    checkresults = rss._feed_check(mockbot, feedreader_feed_valid, 'nohashsign', 'newname')
    expected = [rss.MESSAGES['channel_must_start_with_a_hash_sign'].format('nohashsign')]
    assert expected == checkresults


def test_feed_check_feed_invalid(mockbot, feedreader_feed_invalid):
    checkresults = rss._feed_check(mockbot, feedreader_feed_invalid, '#channel', 'newname')
    expected = [rss.MESSAGES['unable_to_read_feed'].format('nohashsign')]
    assert expected == checkresults


def test_feed_check_feed_item_must_have_title_or_description(mockbot, feedreader_feed_item_neither_title_nor_description):
    checkresults = rss._feed_check(mockbot, feedreader_feed_item_neither_title_nor_description, '#newchannel', 'newname')
    expected = [rss.MESSAGES['feed_items_have_neither_title_nor_description']]
    assert expected == checkresults


def test_feed_delete_delete_db_table(mockbot):
    rss._feed_add(mockbot, '#channel', 'feedname', FEED_VALID)
    rss._feed_delete(mockbot, 'feedname')
    result = rss._db_check_if_table_exists(mockbot, 'feedname')
    assert [] == result


def test_feed_delete_delete_ring_buffer(mockbot):
    rss._feed_add(mockbot, '#channel', 'feedname', FEED_VALID)
    rss._feed_delete(mockbot, 'feedname')
    assert 'feedname' not in bot.memory['rss']['hashes']


def test_feed_delete_delete_feed(mockbot):
    rss._feed_add(mockbot, 'channel', 'feed', FEED_VALID)
    rss._feed_delete(mockbot, 'feed')
    assert 'feed' not in bot.memory['rss']['feeds']


def test_feed_exists_passes(mockbot):
    assert rss._feed_exists(mockbot, 'feed1')


def test_feed_exists_fails(mockbot):
    assert rss._feed_exists(mockbot, 'nofeed') is False


def test_feed_list_format(mockbot):
    rss._feed_add(mockbot, 'channel', 'feed', FEED_VALID, 'f=ft+ftldsapg')
    rss._feed_list(mockbot, 'feed')
    expected = 'channel feed ' + FEED_VALID + ' f=ft+ftldsapg\n'
    assert expected == bot.output


def test_feed_update_messages(mockbot, feedreader_feed_valid):
    rss._feed_update(mockbot, feedreader_feed_valid, 'feed1', True)
    expected = '\x02[feed1]\x02 Title 1 \x02→\x02 https://www.site1.com/article1\n\x02[feed1]\x02 Title 2 \x02→\x02 https://www.site1.com/article2\n\x02[feed1]\x02 Title 3 \x02→\x02 https://www.site1.com/article3\n'
    assert expected == bot.output


def test_feed_update_store_hashes(mockbot, feedreader_feed_valid):
    rss._feed_update(mockbot, feedreader_feed_valid, 'feed1', True)
    expected = ['9696cda86d9a337b37d1f4540c0f5d82', 'dc3088a287c801eb1087020dafee3d85', 'edc845b416110abf9a800552074cb415']
    hashes = bot.memory['rss']['hashes']['feed1'].get()
    assert expected == hashes


def test_feed_update_no_update(mockbot, feedreader_feed_valid):
    rss._feed_update(mockbot, feedreader_feed_valid, 'feed1', True)
    bot.output = ''
    rss._feed_update(mockbot, feedreader_feed_valid, 'feed1', False)
    assert '' == bot.output


def test_hashes_read(mockbot, feedreader_feed_valid):
    rss._feed_update(mockbot, feedreader_feed_valid, 'feed1', True)
    expected = ['9696cda86d9a337b37d1f4540c0f5d82', 'dc3088a287c801eb1087020dafee3d85', 'edc845b416110abf9a800552074cb415']
    bot.memory['rss']['hashes']['feed1'] = rss.RingBuffer(100)
    rss._hashes_read(mockbot, 'feed1')
    hashes = bot.memory['rss']['hashes']['feed1'].get()
    assert expected == hashes


def test_help_config_formats(mockbot):
    rss._help_config(mockbot, ['help', 'config', 'formats'])
    expected = rss.CONFIG['formats']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    for message in rss.CONFIG['formats']['helptext']:
        expected += message + '\n'
    expected += rss.MESSAGES['examples'] + '\n'
    for message in rss.CONFIG['formats']['examples']:
        expected += message.format(mockbot.config.core.prefix) + '\n'
    assert expected == bot.output


def test_help_text_del(mockbot):
    rss._help_text(mockbot, rss.COMMANDS, 'del')
    expected = rss.COMMANDS['del']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    for message in rss.COMMANDS['del']['helptext']:
        expected += message + '\n'
    expected += rss.MESSAGES['examples'] + '\n'
    for message in rss.COMMANDS['del']['examples']:
        expected += message.format(mockbot.config.core.prefix) + '\n'
    assert expected == bot.output


def test_rss_add_feed_add(mockbot):
    rss._rss_add(mockbot, ['add', '#channel', 'feedname', FEED_VALID])
    assert rss._feed_exists(mockbot, 'feedname')


def test_rss_config_feeds_list(mockbot):
    rss._rss_add(mockbot, ['add', '#channel2', 'feed2', FEED_VALID, 'f=p+tlpas'])
    rss._rss_formats(mockbot, ['format', 'feed1', 'f=asl+als'])
    bot.output = ''
    args = ['config', 'feeds']
    rss._rss_config(mockbot, args)
    expected = '#channel1' + rss.CONFIG_SEPARATOR + 'feed1' + rss.CONFIG_SEPARATOR + 'https://www.site1.com/feed' + rss.CONFIG_SEPARATOR + \
        'f=asl+als,#channel2' + rss.CONFIG_SEPARATOR + 'feed2' + rss.CONFIG_SEPARATOR + FEED_VALID + rss.CONFIG_SEPARATOR + 'f=p+tlpas\n'
    assert expected == bot.output


def test_rss_config_formats_default(mockbot):
    rss._rss_config(mockbot, ['config', 'formats'])
    expected = 'f=' + rss.FORMAT_DEFAULT + '\n'
    assert expected == bot.output


def test_rss_config_formats_list(mockbot):
    bot.memory['rss']['formats'] = ['lts+flts', 'at+at']
    args = ['config', 'formats']
    rss._rss_config(mockbot, args)
    expected = 'f=lts+flts;f=at+at;f=fl+ftl' + '\n'
    assert expected == bot.output


def test_rss_config_formats_output(mockbot):
    rss._rss_config(mockbot, ['config', 'formats', 'f=t+t'])
    rss._rss_add(mockbot, ['add', '#channel', 'feedname', FEED_VALID])
    bot.output = ''
    rss._rss_get(mockbot, ['get', 'feedname'])
    expected = 'Title 1\nTitle 2\nTitle 3\n'
    assert expected == bot.output


def test_rss_formats_input_invalid(mockbot):
    rss._rss_config(mockbot, ['config', 'formats', 'fl+fty'])
    bot.output = ''
    rss._rss_config(mockbot, ['config', 'formats'])
    expected = 'f=fl+ftl\n'
    assert expected == bot.output


def test_rss_config_templates_list(mockbot):
    bot.memory['rss']['templates']['t'] = '†{}†'
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|{};t=t|†{}†;t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_invalid_escape_sequence(mockbot):
    template = rss.ESCAPE_CHARACTER + '22{}' + rss.ESCAPE_CHARACTER + '20'
    bot.memory['rss']['templates']['d'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|{};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_invalid_backgroundcolor(mockbot):
    template = rss.ESCAPE_CHARACTER + '04$20{}' + rss.ESCAPE_CHARACTER + '20'
    bot.memory['rss']['templates']['d'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|{};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_light_green_foreground(mockbot):
    template = rss.ESCAPE_CHARACTER + '09{}' + rss.ESCAPE_CHARACTER + '20'
    bot.memory['rss']['templates']['d'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|%09{}%20;t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|{};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_pink_on_silver(mockbot):
    template = rss.ESCAPE_CHARACTER + '13$15{}' + rss.ESCAPE_CHARACTER + '20'
    bot.memory['rss']['templates']['d'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|%13$15{}%20;t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|{};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_output_escape_character(mockbot):
    template = rss.ESCAPE_CHARACTER + rss.ESCAPE_CHARACTER + '{}'
    bot.memory['rss']['templates']['s'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|%%{};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_output_dollar(mockbot):
    template = rss.ESCAPE_CHARACTER + '${}'
    bot.memory['rss']['templates']['s'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|%${};t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_templates_output_dollar_after_control_sequence(mockbot):
    template = rss.ESCAPE_CHARACTER + '17' + rss.ESCAPE_CHARACTER + '${}%16'
    bot.memory['rss']['templates']['s'] = template
    args = ['config', 'templates']
    rss._rss_config(mockbot, args)
    expected = 't=a|<{}>;t=d|{};t=f|%16[{}]%16;t=g|{};t=l|%16→%16 {};'
    expected += 't=p|({});t=s|%17%${}%16;t=t|{};t=y|%16→%16 {}\n'
    expected += rss._config_templates_example(mockbot) + '\n'
    assert expected == bot.output


def test_rss_config_invalid_key(mockbot):
    rss._rss_config(mockbot, ['config', 'invalidkey'])
    expected = ''
    assert expected == bot.output


def test_rss_colors(mockbot):
    rss._rss_colors(mockbot, ['colors'])
    expected = '\x0301,00 00: white \x0f\x0300,01 01: black \x0f\x0300,02 02: blue \x0f\x0300,03 03: green \x0f\x0301,04 04: red \x0f\x0300,05 05: brown \x0f\x0300,06 06: purple \x0f\x0301,07 07: orange \x0f\x0301,08 08: yellow \x0f\x0301,09 09: lime \x0f\x0300,10 10: cyan \x0f\x0301,11 11: aqua \x0f\x0301,12 12: azure \x0f\x0301,13 13: pink \x0f\x0300,14 14: grey \x0f\x0301,15 15: silver \x0f\x0300,01 16: \x02bold\x02 \x0f\x0301,00 17: \x1ditalic\x1d \x0f\x0300,01 18: \x1funderline\x1f \x0f\n'  # noqa: E501
    assert expected == bot.output


def test_rss_del_feed_nonexistent(mockbot):
    rss._rss_del(mockbot, ['del', 'abcd'])
    expected = rss.MESSAGES['feed_does_not_exist'].format('abcd') + '\n'
    assert expected == bot.output


def test_rss_del_feed_delete(mockbot):
    rss._rss_add(mockbot, ['add', '#channel', 'feedname', FEED_VALID])
    rss._rss_del(mockbot, ['del', 'feedname'])
    assert rss._feed_exists(mockbot, 'feedname') is False


def test_rss_fields_feed_nonexistent(mockbot):
    rss._rss_fields(mockbot, ['fields', 'abcd'])
    expected = rss.MESSAGES['feed_does_not_exist'].format('abcd') + '\n'
    assert expected == bot.output


def test_rss_fields_get_default(mockbot):
    rss._rss_fields(mockbot, ['fields', 'feed1'])
    expected = rss.MESSAGES['fields_of_feed'].format('feed1', 'fadglpsty') + '\n'
    assert expected == bot.output


def test_rss_fields_get_custom(mockbot):
    rss._rss_add(mockbot, ['add', '#channel', 'feedname', FEED_VALID, 'f=fltp+atl'])
    bot.output = ''
    rss._rss_fields(mockbot, ['fields', 'feedname'])
    expected = rss.MESSAGES['fields_of_feed'].format('feedname', 'fadglpsty') + '\n'
    assert expected == bot.output


def test_rss_formats_feed_nonexistent(mockbot):
    rss._rss_formats(mockbot, ['format', 'abcd'])
    expected = rss.MESSAGES['feed_does_not_exist'].format('abcd') + '\n'
    assert expected == bot.output


def test_rss_formats_feed_get(mockbot):
    rss._rss_formats(mockbot, ['format', 'feed1', 'f=yt+ytl'])
    bot.output = ''
    rss._rss_formats(mockbot, ['format', 'feed1'])
    expected = 'f=yt+ytl\n'
    assert expected == bot.output


def test_rss_formats_format_unchanged(mockbot):
    format_old = bot.memory['rss']['options']['feed1'].get_format()
    rss._rss_formats(mockbot, ['format', 'feed1', 'f=abcd+efgh'])
    format_new = bot.memory['rss']['options']['feed1'].get_format()
    assert format_old == format_new
    expected = rss.MESSAGES['consider_rss_fields'].format(mockbot.config.core.prefix, 'feed1') + '\n'
    assert expected == bot.output


def test_rss_formats_format_changed(mockbot):
    format_old = bot.memory['rss']['options']['feed1'].get_format()
    rss._rss_formats(mockbot, ['format', 'feed1', 'f=asl+als'])
    format_new = bot.memory['rss']['options']['feed1'].get_format()
    assert format_old != format_new


def test_rss_formats_format_set(mockbot):
    rss._rss_formats(mockbot, ['format', 'feed1', 'f=asl+als'])
    format_new = bot.memory['rss']['options']['feed1'].get_format()
    assert 'f=asl+als' == format_new


def test_rss_formats_format_output(mockbot_rss_update):
    rss._rss_formats(mockbot_rss_update, ['format', 'feed1', 'f=fadglpst+fadglpst'])
    rss._rss_update(mockbot_rss_update, ['update'])
    expected = 'f=fadglpst+fadglpst' + '''
\x02[feed1]\x02 <Author 1> Description of article 1 1 at https://www.site1.com/ \x02→\x02 https://www.site1.com/article1 (2016-08-21 01:10) Description of article 1 Title 1
\x02[feed1]\x02 <Author 2> Description of article 2 2 at https://www.site1.com/ \x02→\x02 https://www.site1.com/article2 (2016-08-22 02:20) Description of article 2 Title 2
\x02[feed1]\x02 <Author 3> Description of article 3 3 at https://www.site1.com/ \x02→\x02 https://www.site1.com/article3 (2016-08-23 03:30) Description of article 3 Title 3
'''
    assert expected == mockbot_rss_update.output


def test_rss_formats_changes_are_saved(mockbot):
    rss._rss_formats(mockbot, ['format', 'feed1', 'f=asl+als'])
    expected = ['#channel1;feed1;https://www.site1.com/feed;f=asl+als']
    assert expected == bot.config.rss.feeds


def test_rss_get_feed_nonexistent(mockbot):
    rss._rss_get(mockbot, ['get', 'abcd'])
    expected = rss.MESSAGES['feed_does_not_exist'].format('abcd') + '\n'
    assert expected == bot.output


def test_rss_get_post_feed_items(mockbot):
    rss._feed_add(mockbot, '#channel', 'feedname', FEED_VALID)
    rss._rss_get(mockbot, ['get', 'feedname'])
    expected = '\x02[feedname]\x02 Title 1 \x02→\x02 https://www.site1.com/article1\n\x02[feedname]\x02 Title 2 \x02→\x02 https://www.site1.com/article2\n\x02[feedname]\x02 Title 3 \x02→\x02 https://www.site1.com/article3\n'  # noqa: E501
    assert expected == bot.output


def test_rss_get_feed_spy(mockbot):
    rss._feed_add(mockbot, '#channel', 'SPY', FEED_SPY)
    rss._rss_get(mockbot, ['get', 'SPY'])
    expected = '\x02[SPY]\x02 Deutsche Bank Predicts 10% Pullback in S&P 500 \x02→\x02 https://markets.financialcontent.com/stocks/news/read?GUID=32821698&Symbol=SPY\n'
    assert expected == bot.output


def test_rss_help_synopsis_help(mockbot):
    rss._rss_help(mockbot, ['help'])
    expected = rss.COMMANDS['help']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    expected += rss.MESSAGES['command_is_one_of'].format('|'.join(sorted(rss.COMMANDS.keys()))) + '\n'
    assert expected == bot.output


def test_rss_help_add(mockbot):
    rss._rss_help(mockbot, ['help', 'add'])
    expected = rss.COMMANDS['add']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    for message in rss.COMMANDS['add']['helptext']:
        expected += message + '\n'
    expected += rss.MESSAGES['examples'] + '\n'
    for message in rss.COMMANDS['add']['examples']:
        expected += message.format(mockbot.config.core.prefix) + '\n'
    assert expected == bot.output


def test_rss_help_config(mockbot):
    rss._rss_help(mockbot, ['help', 'config'])
    expected = rss.COMMANDS['config']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    for message in rss.COMMANDS['config']['helptext']:
        expected += message + '\n'
    expected += rss.MESSAGES['examples'] + '\n'
    for message in rss.COMMANDS['config']['examples']:
        expected += message.format(mockbot.config.core.prefix) + '\n'
    expected += rss.MESSAGES['get_help_on_config_keys_with'].format(mockbot.config.core.prefix, '|'.join(sorted(rss.CONFIG.keys()))) + '\n'
    assert expected == bot.output


def test_rss_help_config_templates(mockbot):
    rss._rss_help(mockbot, ['help', 'config', 'templates'])
    expected = rss.CONFIG['templates']['synopsis'].format(mockbot.config.core.prefix) + '\n'
    for message in rss.CONFIG['templates']['helptext']:
        expected += message + '\n'
    expected += rss.MESSAGES['examples'] + '\n'
    for message in rss.CONFIG['templates']['examples']:
        expected += message.format(mockbot.config.core.prefix) + '\n'
    assert expected == bot.output


def test_rss_join(mockbot):
    rss._rss_join(mockbot, ['join'])
    channels = []
    for feed in bot.memory['rss']['feeds']:
        feedchannel = bot.memory['rss']['feeds'][feed]['channel']
        if feedchannel not in channels:
            channels.append(feedchannel)
    assert channels == bot.config.core.channels


def test_rss_list_all(mockbot_rss_list):
    rss._rss_list(mockbot_rss_list, ['list'])
    expected1 = '#channel1 feed1 https://www.site1.com/feed'
    expected2 = '#channel2 feed2 https://www.site2.com/feed'
    assert expected1 in mockbot_rss_list.output
    assert expected2 in mockbot_rss_list.output


def test_rss_list_feed(mockbot):
    rss._rss_list(mockbot, ['list', 'feed1'])
    expected = '#channel1 feed1 https://www.site1.com/feed\n'
    assert expected == bot.output


def test_rss_list_channel(mockbot):
    rss._rss_list(mockbot, ['list', '#channel1'])
    expected = '#channel1 feed1 https://www.site1.com/feed\n'
    assert expected == bot.output


def test_rss_list_no_feed_found(mockbot):
    rss._rss_list(mockbot, ['list', 'invalid'])
    assert '' == bot.output


def test_rss_templates_get_default(mockbot):
    rss._rss_templates(mockbot, ['templates', 'feed1'])
    assert '' == bot.output


def test_rss_templates_get_custom(mockbot):
    rss._rss_templates(mockbot, ['templates', 'feed1', 't=f|%06%16[{}]%20'])
    bot.output = ''
    rss._rss_templates(mockbot, ['templates', 'feed1'])
    expected = 't=f|%06%16[{}]%20\n\x0306\x02[feed1]\x0f Title \x02→\x02 https://github.com/RebelCodeBase/sopel-rss\n'
    assert expected == bot.output


def test_rss_templates_set(mockbot):
    rss._rss_templates(mockbot, ['templates', 'feed1', 't=f|%06%16[{}]%20'])
    expected = 't=f|%06%16[{}]%20\n\x0306\x02[feed1]\x0f Title \x02→\x02 https://github.com/RebelCodeBase/sopel-rss\n'
    assert expected == bot.output


def test_rss_templates_override(mockbot):
    format_add = 'f=l+agpt'
    templates_add = 't=t' + rss.TEMPLATE_SEPARATOR + 'addtitle:{}'
    templates_add += rss.CONFIG_SEPARATOR
    templates_add += 't=g' + rss.TEMPLATE_SEPARATOR + 'addguid:{}'
    options = templates_add + rss.CONFIG_SEPARATOR + format_add
    templates_feed = 't=t' + rss.TEMPLATE_SEPARATOR + 'feedtitle:{}'
    templates_feed += rss.CONFIG_SEPARATOR
    templates_feed += 't=a' + rss.TEMPLATE_SEPARATOR + 'feedauthor:{}'
    templates_default = 't=t' + rss.TEMPLATE_SEPARATOR + 'defaulttitle:{}'
    templates_default += rss.CONFIG_SEPARATOR
    templates_default += 't=p' + rss.TEMPLATE_SEPARATOR + 'defaultpublished:{}'
    templates_default += rss.CONFIG_SEPARATOR
    templates_default += 't=g' + rss.TEMPLATE_SEPARATOR + 'defaultguid:{}'
    rss._rss_add(mockbot, ['add', '#channel', 'feed', FEED_VALID, options])
    rss._rss_templates(mockbot, ['templates', 'feed', templates_feed])
    rss._rss_config(mockbot, ['config', 'templates', templates_default])
    bot.output = ''
    rss._rss_get(mockbot, ['get', 'feed'])
    expected = 'feedauthor:Author 1 addguid:1 at https://www.site1.com/ defaultpublished:2016-08-21 01:10 feedtitle:Title 1\nfeedauthor:Author 2 addguid:2 at https://www.site1.com/ defaultpublished:2016-08-22 02:20 feedtitle:Title 2\nfeedauthor:Author 3 addguid:3 at https://www.site1.com/ defaultpublished:2016-08-23 03:30 feedtitle:Title 3\n'  # noqa: E501
    assert expected == bot.output


def test_rss_templates_changes_are_saved(mockbot):
    rss._rss_templates(mockbot, ['format', 'feed1', 't=t|...{}...'])
    expected = ['#channel1;feed1;https://www.site1.com/feed;t=t|...{}...']
    assert expected == bot.config.rss.feeds


def test_rss_update_update(mockbot_rss_update):
    rss._rss_update(mockbot_rss_update, ['update'])
    expected = '\x02[feed1]\x02 Title 1 \x02→\x02 https://www.site1.com/article1\n\x02[feed1]\x02 Title 2 \x02→\x02 https://www.site1.com/article2\n\x02[feed1]\x02 Title 3 \x02→\x02 https://www.site1.com/article3\n'
    assert expected == mockbot_rss_update.output


def test_rss_update_no_update(mockbot_rss_update):
    rss._rss_update(mockbot_rss_update, ['update'])
    bot.output = ''
    rss._rss_update(mockbot_rss_update, ['update'])
    assert '' == bot.output


def test_options_get_format_custom(mockbot, feedreader_feed_valid):
    options = rss.Options(mockbot, feedreader_feed_valid, 'f=ta+ta')
    assert 'f=ta+ta' == options.get_format()


def test_options_get_format_default(mockbot, feedreader_feed_valid):
    options = rss.Options(mockbot, feedreader_feed_valid)
    assert options.get_format_default() == options.get_format()


def test_options_get_fields_feed_valid(mockbot, feedreader_feed_valid):
    options = rss.Options(mockbot, feedreader_feed_valid)
    fields = options.get_fields()
    assert 'fadglpsty' == fields


def test_options_get_fields_feed_item_neither_title_nor_description(mockbot, feedreader_feed_item_neither_title_nor_description):
    options = rss.Options(mockbot, feedreader_feed_item_neither_title_nor_description)
    fields = options.get_fields()
    assert 'd' not in fields and 't' not in fields


def test_options_check_format_default(mockbot, feedreader_feed_valid):
    options = rss.Options(mockbot, feedreader_feed_valid)
    assert options.get_format_default() == options.get_format()


def test_options_check_format_hashed_empty(mockbot, feedreader_feed_valid):
    format = 'f=+t'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_output_empty(mockbot, feedreader_feed_valid):
    format = 'f=t'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_hashed_only_feedname(mockbot, feedreader_feed_valid):
    format = 'f=f+t'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_output_only_feedname(mockbot, feedreader_feed_valid):
    format = 'f=t+f'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_duplicate_separator(mockbot, feedreader_feed_valid):
    format = 'f=t+t+t'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_duplicate_field_hashed(mockbot, feedreader_feed_valid):
    format = 'f=ll+t'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_duplicate_field_output(mockbot, feedreader_feed_valid):
    format = 'f=l+tll'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format != options.get_format()


def test_options_check_format_tinyurl(mockbot, feedreader_feed_valid):
    format = 'f=fy+ty'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    assert format == options.get_format()


def test_options_check_tinyurl_output(mockbot, feedreader_feed_valid):
    format = 'f=fy+ty'
    options = rss.Options(mockbot, feedreader_feed_valid, format)
    item = feedreader_feed_valid.get_feed().entries[0]
    post = options.get_post('feed1', item)
    expected = 'Title 3 \x02→\x02 https://tinyurl.com/govvpmm'
    assert expected == post


def test_options_check_template_valid(mockbot):
    template = '{}'
    result = rss.Options(mockbot, rss.FeedReader('')).is_template_valid(template)
    assert result is True


def test_options_check_template_invalid_no_curly_braces(mockbot):
    template = ''
    result = rss.Options(mockbot, rss.FeedReader('')).is_template_valid(template)
    assert result is False


def test_options_check_template_invalid_duplicate_curly_braces(mockbot):
    template = '{}{}'
    result = rss.Options(mockbot, rss.FeedReader('')).is_template_valid(template)
    assert result is False


def test_options_set_get_templates(mockbot):
    templates = 't=a' + rss.TEMPLATE_SEPARATOR + '((({})))'
    templates += rss.CONFIG_SEPARATOR
    templates += 't=s' + rss.TEMPLATE_SEPARATOR + '->{}<-'
    bot.memory['rss']['options']['feed1'].set_templates(templates)
    templates_after = bot.memory['rss']['options']['feed1'].get_templates()
    assert templates == templates_after


def test_ringbuffer_append():
    rb = rss.RingBuffer(3)
    assert rb.get() == []
    rb.append('1')
    assert ['1'] == rb.get()


def test_ringbuffer_overflow():
    rb = rss.RingBuffer(3)
    rb.append('hash1')
    rb.append('hash2')
    rb.append('hash3')
    assert ['hash1', 'hash2', 'hash3'] == rb.get()
    rb.append('hash4')
    assert ['hash2', 'hash3', 'hash4'] == rb.get()
