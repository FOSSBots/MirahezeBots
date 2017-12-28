from __future__ import unicode_literals, absolute_import, print_function, division
from sopel.module import commands
import platform


@commands('python', 'pyver')
def pythonversion(bot, trigger):
    """Reply with Python version bot is running."""
    bot.say("I am running Python " + platform.python_version() + ".")
