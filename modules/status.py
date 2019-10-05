# Pastebin xEWKC8sO
#!/usr/bin/env python3.6
import configparser, json, mwclient
from mwclient import errors
import QuIRC
import random
import requests
import re
import time
lastuser = ''
pages = ''

bot = QuIRC.IRCConnection()

def on_connect(bot):
    bot.set_nick("RF1_Bot")
    bot.send_user_packet("RF1_Bot")

def on_welcome(bot):
    bot.send_message('NickServ', 'identify ')
    print('Authed to NickServ')
    time.sleep(10)
    bot.join_channel('##wikimedia-statuschange')
def save_wrap(site):
    print('line 9')
    global pages
    global contents
    pagename1 = 'User:RhinosF1/Status'
    page1 = site.Pages[pagename1]
    content1 = contents
    print('Line 13')
    #print('Content: ' + content1)
    pages = pagename1
    save_edit(page1, site, content1)
    print('Line 17')

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
        if 'rhinosf1' == sender.lower():
            if __name__ == "__main__":
                main()
        else:
            if lastuser == sender.lower():
                bot.send_message(sender, 'You have been quited for misuse of ##wikimedia-statuschange')
                bot.send_message('RhinosF1', (str(sender) + ':quited in ##wikimedia-statuschange, +z activated'))
                message = str('flags ##wikimedia-statuschange ' + sender + " -e+q")
                print(message)
                bot.send_message('ChanServ', message)
                message2 = 'quiet ##wikimedia-statuschange ' + sender
                print(message2)
                bot.send_message('ChanServ', message2)
                bot.send_message('ChanServ', 'set mlock ##wikimedia-statuschange +z')
            else:
                bot.send_message(sender, 'You can not use !run')
                bot.send_message('RhinosF1', (str(sender) + ' attempted to use !run'))
                lastuser = sender
    if  '!stop' == message.lower():
        if 'rhinosf1' == sender.lower():
            quit()
        else:
            if lastuser == sender.lower():
                bot.send_message(sender, 'You have been quited for misuse of ##wikimedia-statuschange')
                bot.send_message('RhinosF1', (str(sender) + ':quited in ##wikimedia-statuschange, +z activated'))
                message = str('flags ##wikimedia-statuschange ' + sender + " -e+q")
                print(message)
                bot.send_message('ChanServ', message)
                message2 = 'quiet ##wikimedia-statuschange ' + sender
                print(message2)
                bot.send_message('ChanServ', message2)
                bot.send_message('ChanServ', 'set mlock ##wikimedia-statuschange +z')
            else:
                bot.send_message(sender, 'You can not use !stop')
                bot.send_message('RhinosF1', (str(sender) + ' attempted to use !stop'))
                lastuser = sender

    
bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)
bot.connect("chat.freenode.net")
bot.run_loop()
