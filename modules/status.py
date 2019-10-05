import configparser, json, mwclient
from mwclient import errors
import random
import requests
import re
import time
from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import rule, commands, example
pages = ''

def save_wrap(site):
    page = site.Pages['User:' + requester + '/Status']
    content = status
    save_edit(page, content)

def save_edit(page, content):
    time.sleep(5)
    edit_summary = """BOT: Settings status per request """
    times = 0
    while True:
        if times > 1:
            break
        try:
            page.save(content, summary=edit_summary, bot=True, minor=True)
            print('Line 27')
        except errors.ProtectedPageError:
            print('Could not edit ' + page + ' due to protection')
            times += 1
        except errors.EditError:
            print("Error")
            times += 1
            time.sleep(5)  # sleep for 5 seconds before trying again
            continue
        break




def main():
    site = mwclient.Site(('https', wiki + '.miraheze.org'), '/w/')
    config = configparser.RawConfigParser()
    config.read('credentials.txt')
    try:
        site.login(config.get('enwiki_sandbot', 'username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
    save_wrap(site)
    

@commands('status')
@example('.status mhtest offline')
def status(bot, trigger):
    try:
        options = trigger.group(2).split(" ")
        if len(options) == 3:
            wiki = options[0]
            user = options[1]
            status = options[2]
            host = trigger.host
            host = host.split('/')
            if host[0] = 'miraheze':
                requester = host[1]
                if __name__ == "__main__":
                    main()
                 return wiki
                 return requester
                 return status
    except AttributeError:
        bot.say('Syntax: .mh wiki page', trigger.sender)

    
