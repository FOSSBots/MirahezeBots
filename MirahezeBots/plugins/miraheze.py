"""This plugin contains miraheze specific commands."""
from sopel.plugin import commands, example, rule
from sopel import bot, trigger

MIRAHEZE_ABOUT_MIRAHEZE_CHANNEL = (
    'Miraheze is a non-profit wikifarm running MediaWiki. If you would like '
    'more information please see '
    'https://meta.miraheze.org/ or ask in this channel.'
)
MIRAHEZE_ABOUT_OTHER_CHANNELS = (
    'Miraheze is a non-profit wikifarm running MediaWiki. If you would like '
    'more information please see '
    'https://meta.miraheze.org/ or #miraheze.'
)


@commands('miraheze')
@rule('.*[w-wW-W]hat (even is [m-mM-M]iraheze|is [m-mM-M]iraheze|does [m-mM-M]iraheze do).*')
@example('.miraheze')
def miraheze(instance: bot, message: trigger) -> None:
    """Tells you about Miraheze and where to learn more."""
    if message.sender == '#miraheze':
        instance.reply(MIRAHEZE_ABOUT_MIRAHEZE_CHANNEL)
    else:
        instance.reply(MIRAHEZE_ABOUT_OTHER_CHANNELS)


@commands('gethelp')
@rule("([i-iI-I] need help|[c-cC-C]an someone help me|[i-iI-I] can(t|'t) login).*")
@example('.gethelp I cannot access https://meta.miraheze.org')
def miraheze_gethelp(instance: bot, message: trigger) -> None:
    """Reply to help requests."""
    if message.sender == '#miraheze':
        instance.reply(
            'Pinging dmehus, Reception123, RhinosF1, Southparkfan, Universal_Omega and Voidwalker,'
            'who might be able to help you. Other users in this channel also see this and may be able to assist you.')
    else:
        instance.reply('If you need Miraheze releated help, please join #miraheze')


@commands('discord')
def miraheze_discord(instance: bot, message: trigger) -> None:  # noqa: U100
    """Display discord information for Miraheze."""
    instance.reply('You can join discord by going to, https://miraheze.org/discord!')
