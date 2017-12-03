from __future__ import unicode_literals, absolute_import, print_function, division
import sopel
import sopel.module
import requests
import sopel.tools
from sopel.module import rule, priority, thread, commands, example
import sys
import platform

def pythonversion(bot,trigger):
bot.say("I am running Python " + platform.python_version() + ".")
