Changelog

# ZppixBot v2
## Changes since v1
* Added an admin list command (.adminlist)
* Added .accesslevel command
* Added .gethelp command (pings helpful users in channels)
* Added a converse module
* Added a new reminder system

# ZppixBot v3
## New modules added
* mh_phab
* welcome

## Modules updated
* converse
* adminlist
* reminders

# ZppixBot v5
## New modules added
* test_module
* channelmgnt

## Modules changed
* urls
* miraheze
* adminlist

# ZppixBot v6
## Channel Management
* Added option to set channel operators individually for each channel
* Now supports inviting users
* Bug fixes
## Mediawiki Status
* Created to allow users to set a status on mediawiki wikis.
* Compatible user script and template developed by RhinosF1
* See meta.miraheze.org/wiki/Template:UserStatus and https://meta.miraheze.org/wiki/User:RhinosF1/status.js
## Join
* Bug Fixes
## Responses
* Added new ones
* Removed poorly used ones
## Short Links
* Created to allow you to access your favourite sites in fewer clicks
## Urls
* Bug fixes

# ZppixBot v7
## mh_phab
This has been completely rewrote to be more efficent.
We've introduced more config options as well.
## dbclean
This is a new cli script to help clean up databases
## adminlist
Now uses the owner/admin account config rather than nickname.
## channelmgnt
You can now set modes, we've improved documentation and fixed a few bugs
## find_updates
Has been replaced by the upstream version
## joinall (was join)
We've removed the join control and replaced it with joinall that forces the bot to join all channels in your config file
## responses
Has had some merged from other responses and no longer breaks with spaces
## status
Now works with non cloaked users
## welcome
Now also recognises accounts
## Requirements
We changed the way we install things from pip.
You only need to install requirments.txt but you might find pip-install.txt has some more fun modules on.

# MirahezeBot v7.1
With Version 7.1, we bring you a fancy new name as MirahezeBot and some
bug fixes and improvements.

Please note that with this version we no longer support python 3.5, please upgrade to python 3.6 or above.

## Phabricator
This module now supports all phabricator installs with conduit enabled.

## Responses
A support_channel configuration variable was introduced.

## Status
* Removed deceprated tuple
* Introduced support_channel, wiki_username, wiki_password and data_path cnfiguration.
* some functions now use bot.reply

## models
This was incorrectly placed in the modules folder and has been moved to tests.

# MirahezeBot v7.2
## Status
- Removed modules/config/*.csv
## Responses
- Bug fixes
## channelmgnt
- Switched to a new json config system

# MirahezeBot v8.0.0
In this update, we switch to using PyPi to install rather than copying to the plugins/modules folder. You should now delete our plugins from the plugins/modules folder and must switch to using PyPi to install. The minimum sopel version is now 7.0.5. Other requirements have changed. Please review compatibility with your install.
## goofy
- This new fun module was added
## dbclean
- This is now wrapped in a main() script and can be called using 'sopel-dbclean'
## mh_phab --> phab
- Bug fixes
- renamed from mh_phab to phab
## responses
- bug fixes
## shortlinks
- bug fixes
## Status
- minor correction to help text

