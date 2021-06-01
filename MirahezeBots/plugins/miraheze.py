"""This plugin contains miraheze specific commands."""
from sopel.plugin import commands, example, rule

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
def miraheze(bot, trigger):
    """Tells you about Miraheze and where to learn more."""
    if trigger.sender == '#miraheze':
        bot.reply(MIRAHEZE_ABOUT_MIRAHEZE_CHANNEL)
    else:
        bot.reply(MIRAHEZE_ABOUT_OTHER_CHANNELS)


@commands('gethelp')
@rule("([i-iI-I] need help|[c-cC-C]an someone help me|[i-iI-I] can(t|'t) login).*")
@example('.gethelp I cannot access https://meta.miraheze.org')
def miraheze_gethelp(bot, trigger):
    """Reply to help requests."""
    if trigger.sender == '#miraheze':
        bot.reply(
            'Pinging dmehus, JohnLewis, paladox, Reception123, RhinosF1, SPF|Cloud, Universal_Omega and Voidwalker,'
            'who might be able to help you. Other users in this channel also see this and may be able to assist you.')
    else:
        bot.reply('If you need Miraheze releated help, please join #miraheze')


@commands('discord')
def miraheze_discord(bot, trigger):  # noqa: U100
    """Display discord information for Miraheze."""
    bot.reply('You can join discord by going to, https://miraheze.org/discord!')
