"""This plugin expands links to various websites."""
from sopel.plugin import commands, example
from sopel import bot, trigger


@commands('github', 'gh')
@example('.github user')
def ghuser(instance: bot, message: trigger) -> None:
    """Expand a link to github."""
    try:
        instance.say(f'https://github.com/{message.group(2)}')
    except TypeError:
        instance.say('Syntax: .github user', message.sender)


@commands('redditu')
@example('.redditu example')
def redditu(instance: bot, message: trigger) -> None:
    """Expand a link to reddit/u."""
    try:
        instance.say(f'https://reddit.com/u/{message.group(2)}')
    except TypeError:
        instance.say('Syntax: .redditu example', message.sender)


@commands('subred')
@example('.subred example')
def redditr(instance: bot, message: trigger) -> None:
    """Expand a link to reddit/r."""
    try:
        instance.say(f'https://reddit.com/r/{message.group(2)}')
    except TypeError:
        instance.say('Syntax: .subred example', message.sender)


@commands('wmca')
@example('.wmca example')
def wmca(instance: bot, message: trigger) -> None:
    """Expand a link to Wikimedia CentralAuth."""
    try:
        instance.say(
            f'https://meta.wikimedia.org/wiki/Special:CentralAuth/{message.group(2).replace(" ", "_")}'
            )
    except AttributeError:
        instance.say('Syntax: .wmca example', message.sender)


@commands('mhca')
@example('.mhca example')
def mhca(instance: bot, message: trigger) -> None:
    """Expand a link to Miraheze Central Auth."""
    try:
        instance.say(
            f'https://meta.miraheze.org/wiki/Special:CentralAuth/{message.group(2).replace(" ", "_")}'
            )
    except AttributeError:
        instance.say('Syntax: .mhca example', message.sender)


@commands('tw')
@example('.tw user')
def twlink(instance: bot, message: trigger) -> None:
    """Expand a link to Twitter."""
    try:
        instance.say(f'https://twitter.com/{message.group(2)}')
    except TypeError:
        instance.say('Syntax: .tw user', message.sender)


@commands('mh')
@example('.mh wiki page')
def mhwiki(instance: bot, message: trigger) -> None:
    """Expand a link to Miraheze wikis."""
    try:
        options = message.group(2).split(' ', 1)
        if len(options) == 1:
            instance.say(
                f'https://meta.miraheze.org/wiki/{options[0].replace(" ", "_")}'
                )
        elif len(options) == 2:
            wiki = options[0]
            page = options[1].replace(' ', '_')
            instance.say(f'https://{wiki}.miraheze.org/wiki/{page}')
    except AttributeError:
        instance.say('Syntax: .mh wiki page', message.sender)
