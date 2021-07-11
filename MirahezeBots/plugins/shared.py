"""Sopel Inter-Plugin resource sharing service."""

from requests import Session
from sopel import bot
from sopel.tools import SopelMemory


def setup(instance: bot) -> None:
    """Create the resources that can be accessed via sopel shared."""
    instance.memory['shared'] = SopelMemory()
    instance.memory['shared']['session'] = Session()
