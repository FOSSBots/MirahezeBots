import configparser, json, mwclient
from mwclient import errors
import QuIRC
import random
import requests
import re
import time
lastuser = ''
pages = ''


def save_edit(page, site, content):
    import time
    global senders
    global pages
    time.sleep(5)
    edit_summary = """BOT: Settings status per request """
    times = 0
    while True:
        if times > 1:
            break
        try:
            page.save(content, summary=edit_summary, bot=True, minor=True)
            print('Line 27')
            bot.send_message('##wikimedia-statuschange', senders + ": I've updated http://en.wikipedia.org/wiki/" + pages )
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
    site = mwclient.Site(('https', 'quirc.miraheze.org'), '/w/')
    config = configparser.RawConfigParser()
    config.read('credentials2.txt')
    print('Line 45')
    try:
        site.login(config.get('enwiki_sandbot', 'username'), config.get('enwiki_sandbot', 'password'))
    except errors.LoginError as e:
        print(e)
        raise ValueError("Login failed.")
    save_wrap(site)

def on_message(bot, channel, sender, message):
    global lastuser
    global senders
    global contents
    if '!run' in message.lower():
        senders = sender
        print(message)
        contents = message.split(' ')
        print(contents)
        contents = contents[1]
        print(contents)
        if __name__ == "__main__":
                main()

    
