"""Sopel Inter-Plugin resource sharing service."""

from requests import Session
from sopel import bot
from sopel.tools import SopelMemory


def setup(bot: bot) -> None:
    """Create the resources that can be accessed via sopel shared."""
    bot.memory['shared'] = SopelMemory()
    bot.memory['shared']['session'] = Session()
