# coding=utf-8
# Copyright 2008, Sean B. Palmer, inamidst.com
# Copyright 2012, Elsie Powell, embolalia.com
# Copyright 2018, Rusty Bower, rustybower.com
# Licensed under the Eiffel Forum License 2.
from __future__ import unicode_literals, absolute_import, print_function, division

from sopel.config.types import StaticSection, ValidatedAttribute
from sopel.module import commands, example, NOLIMIT
from sopel.modules.units import c_to_f

import re
import requests


# Define our sopel weather configuration
class WeatherSection(StaticSection):
    source = ValidatedAttribute('source', str, default='openweathermap')
    api_key = ValidatedAttribute('api_key', str, default='')


def setup(bot):
    bot.config.define_section('weather', WeatherSection)


# Walk the user through defining variables required
def configure(config):
    config.define_section('weather', WeatherSection, validate=False)
    config.weather.configure_setting(
        'api_key',
        'Enter openweathermap.org API Key:'
    )


def search(mode, query, api_key):
    """
    Find the first Where On Earth ID for the given query. Result is the etree
    node for the result, so that location data can still be retrieved. Returns
    None if there is no result, or the woeid field is empty.
    """
    results = None

    # Check if it's a WOEID
    if re.match(r'^w[0-9]+$', query.encode('utf-8').decode('utf-8')):
        # Strip off the w from WOEID
        results = requests.get(
            'https://api.openweathermap.org/data/2.5/%s?id=%s&appid=%s&units=metric' % (mode, query[1:], api_key))
    # Check if zip code (this doesn't cover all, but most)
    # https://en.wikipedia.org/wiki/List_of_postal_codes
    elif re.match(r'^\d+$', query.encode('utf-8').decode('utf-8')):
        results = requests.get(
            'https://api.openweathermap.org/data/2.5/%s?zip=%s&appid=%s&units=metric' % (mode, query, api_key))
    # Otherwise, we assume it's a city name or location
    else:
        results = requests.get(
            'https://api.openweathermap.org/data/2.5/%s?q=%s&appid=%s&units=metric' % (mode, query, api_key))
    if not results or results.status_code != 200:
        return None
    return results.json()


def get_condition(parsed):
    try:
        condition = parsed['weather'][0]['main']
    except (KeyError, TypeError, ValueError):
        return 'unknown'
    return condition


def get_temp(parsed):
    try:
        temp = float(parsed['main']['temp'])
    except (KeyError, TypeError, ValueError):
        return 'unknown'
    return u'%d\u00B0C (%d\u00B0F)' % (round(temp), round(c_to_f(temp)))


def get_humidity(parsed):
    try:
        humidity = parsed['main']['humidity']
    except (KeyError, TypeError, ValueError):
        return 'unknown'
    return "Humidity: %s%%" % humidity


def get_wind(parsed):
    try:
        wind_data = parsed['wind']
        m_s = float(round(wind_data['speed'], 1))
        speed = int(round(m_s * 1.94384, 0))
        degrees = int(wind_data['deg'])
    except (KeyError, TypeError, ValueError):
        return 'unknown'

    if speed < 1:
        description = 'Calm'
    elif speed < 4:
        description = 'Light air'
    elif speed < 7:
        description = 'Light breeze'
    elif speed < 11:
        description = 'Gentle breeze'
    elif speed < 16:
        description = 'Moderate breeze'
    elif speed < 22:
        description = 'Fresh breeze'
    elif speed < 28:
        description = 'Strong breeze'
    elif speed < 34:
        description = 'Near gale'
    elif speed < 41:
        description = 'Gale'
    elif speed < 48:
        description = 'Strong gale'
    elif speed < 56:
        description = 'Storm'
    elif speed < 64:
        description = 'Violent storm'
    else:
        description = 'Hurricane'

    if (degrees <= 22.5) or (degrees > 337.5):
        degrees = u'\u2193'
    elif (degrees > 22.5) and (degrees <= 67.5):
        degrees = u'\u2199'
    elif (degrees > 67.5) and (degrees <= 112.5):
        degrees = u'\u2190'
    elif (degrees > 112.5) and (degrees <= 157.5):
        degrees = u'\u2196'
    elif (degrees > 157.5) and (degrees <= 202.5):
        degrees = u'\u2191'
    elif (degrees > 202.5) and (degrees <= 247.5):
        degrees = u'\u2197'
    elif (degrees > 247.5) and (degrees <= 292.5):
        degrees = u'\u2192'
    elif (degrees > 292.5) and (degrees <= 337.5):
        degrees = u'\u2198'

    return description + ' ' + str(m_s) + 'm/s (' + degrees + ')'


def get_tomorrow_condition(results):
    # Only using the first 8 results to get the next 24 hours (8 * 3 hours)
    # This is super ugly with list comprehensions
    if [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Snow']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Snow'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    elif [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Thunderstorm']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Thunderstorm'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    elif [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Rain']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Rain'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    elif [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Drizzle']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Drizzle'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    elif [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Atmosphere']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Atmosphere'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    elif [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Clouds']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Clouds'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    elif [x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Clear']:
        return sorted([x['weather'][0] for x in results['list'][:8] if x['weather'][0]['main'] == 'Clear'],
                      key=lambda k: k['id'], reverse=True)[0]['description'].title()
    else:
        return 'Unknown'


def get_tomorrow_high(results):
    temp = None
    # Only using the first 8 results to get the next 24 hours (8 * 3 hours)
    for _ in results['list'][:8]:
        if temp is None or _['main']['temp_max'] > temp:
            temp = _['main']['temp_max']
    return u'High: %d\u00B0C (%d\u00B0F)' % (temp, c_to_f(temp))


def get_tomorrow_low(results):
    temp = None
    # Only using the first 8 results to get the next 24 hours (8 * 3 hours)
    for _ in results['list'][:8]:
        if temp is None or _['main']['temp_min'] < temp:
            temp = _['main']['temp_min']
    return u'Low: %d\u00B0C (%d\u00B0F)' % (temp, c_to_f(temp))


def say_info(bot, trigger, mode):
    location = trigger.group(2)
    if not location:
        woeid = bot.db.get_nick_value(trigger.nick, 'woeid')
        if not woeid:
            return bot.reply("I don't know where you live. "
                             "Give me a location, like {pfx}{command} London, "
                             "or tell me where you live by saying {pfx}setlocation "
                             "London, for example.".format(command=trigger.group(1),
                                                           pfx=bot.config.core.help_prefix))
    else:
        location = location.strip()
        woeid = bot.db.get_nick_value(location, 'woeid')
        if woeid is None:
            result = search('weather', location, bot.config.weather.api_key)
            if not result:
                return bot.reply("I don't know where that is.")
            woeid = result['id']

    # Temporary solution because OpenWeatherAPI suddenly started returning 0 for city_id
    if woeid == 0:
        return bot.reply("ERROR: API did not return a WOEID")

    if mode == 'weather':
        # Prepend w to ensure bot knows to search for WOEID
        result = search('weather', 'w' + str(woeid), bot.config.weather.api_key)

        if not result:
            return bot.reply("An error occurred")
        else:
            location = result['name']
            country = result['sys']['country']
            temp = get_temp(result)
            condition = get_condition(result)
            humidity = get_humidity(result)
            wind = get_wind(result)
            return bot.say(u'%s, %s: %s, %s, %s, %s' % (location, country, temp, condition, humidity, wind))

    if mode == 'forecast':
        result = search('forecast', 'w' + str(woeid), bot.config.weather.api_key)

        if not result:
            return bot.reply("An error occurred")
        else:
            location = result['city']['name']
            country = result['city']['country']
            tomorrow_condition = get_tomorrow_condition(result)
            tomorrow_high = get_tomorrow_high(result)
            tomorrow_low = get_tomorrow_low(result)
            return bot.say(u'24h Forecast: %s, %s: %s, %s, %s' % (location, country, tomorrow_condition, tomorrow_high, tomorrow_low))
    return


@commands('weather', 'wea')
@example('.weather')
@example('.weather London')
@example('.weather Seattle, US')
@example('.weather 90210')
@example('.weather w7174408')
def weather_command(bot, trigger):
    """.weather location - Show the weather at the given location."""
    if bot.config.weather.api_key is None or bot.config.weather.api_key == '':
        return bot.reply("API key missing. Please configure this module.")
    return say_info(bot, trigger, 'weather')


@commands('forecast')
@example('.forecast')
@example('.forecast London')
@example('.forecast Seattle, US')
@example('.forecast 90210')
@example('.forecast w7174408')
def forecast_command(bot, trigger):
    """.forecast location - Show the weather forecast for tomorrow at the given location."""
    if bot.config.weather.api_key is None or bot.config.weather.api_key == '':
        return bot.reply("API key missing. Please configure this module.")
    return say_info(bot, trigger, 'forecast')


@commands('setlocation')
@example('.setlocation London')
@example('.setlocation Seattle, US')
@example('.setlocation 90210')
@example('.setlocation w7174408')
def update_location(bot, trigger):
    if bot.config.weather.api_key is None or bot.config.weather.api_key == '':
        return bot.reply("API key missing. Please configure this module.")

    """Set your default weather location."""
    if not trigger.group(2):
        bot.reply('Give me a location, like "London" or "90210" or "w2643743".')
        return NOLIMIT

    result = search('weather', trigger.group(2), bot.config.weather.api_key)

    if not result:
        return bot.reply("I don't know where that is.")

    woeid = result['id']

    bot.db.set_nick_value(trigger.nick, 'woeid', woeid)

    city = result['name']
    country = result['sys']['country'] or ''
    return bot.reply('I now have you at WOEID %s (%s, %s)' %
                     (woeid, city, country))
