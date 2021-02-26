
**Changelog**

Please see below for changes to MirahezeBot-Plugins
# Version 9.1.1
- Fixed developer requirements blocking newer versions of channelmgnt.
# Version 9.1.0
- CI: Migrate to GitHub-Actions
- CI: Support Python 3.9, Windows and MacOS
- dbclean: style changes
- example-db: rename
- adminlist: split to own package
- joinall: split to own package
- phab: use new jsonparser
- pingpong: split to own package
- responses: style changes and switch to VERSION keyword
- rss: style changes
- status: style changes & new jsonparser
- welcome: style changes and remove get_filename, replace with bot.known_users_filename
- jsonparser: split to own package
- version: introduce VERSION, VERSIONARRAY and SHORTVERSION keywords
- Security: Drop support for Sopel 7.0.5 & 7.0.6
- requirements: update some and slacken others
- build: style changes
# Version 9.0.3
- Fixed an issue affecting new installs due to a transient dependancy
# Version 9.0.2
## Security fixes
# Version 9.0.0
## Miscellaneous
- travis: changed test configuration
- responses: corrections and style changes
- rss: style improvements
- test models: style tweaks
- test general: up'd max line length
- test rss: style changes & replaced http:// with https://
## Requirements
- mwclient no longer required
- Setuptools bumped from 49.5.0 to 49.6.0
- flake8 is now required for developers
- SQLAchemy is now at 1.3.19
## Plugins
- all: removed future imports
- channelmgnt: switched to caching the json config
- channelmgnt: introduced a makemodechange system
- channelmgnt: added support_channel config
- status: replaced mwclient with a new util script, introduced cached json config, renamed other config
- phab: Introduced channel specific configuration


# Version 8.0.3
## Miscellaneous
- Changes to the gitignore file & manifest to ensure proper handling of downloads & uploads
- Changes to build configuration to prevent wasted checks
- Cleaner Changelog
## requirements
- Setuptools was bumped from 49.2.0 to 49.2.1 for developers
## phab
- A bug was fixed with the task regex (T57)

# Version 8.0.1 & 8.0.2
- Changes to the build configuartion to prevent PyPi errors

# Version 8.0.0
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

# Version 7.2
## Status
- Removed modules/config/*.csv
## Responses
- Bug fixes
## channelmgnt
- Switched to a new json config system
# Version 7.1
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

# Version 7
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

# Version 6
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

# Version 5
## New modules added
* test_module
* channelmgnt

## Modules changed
* urls
* miraheze
* adminlist

# Version 3
## New modules added
* mh_phab
* welcome

## Modules updated
* converse
* adminlist
* reminders

# Version 2
* Added an admin list command (.adminlist)
* Added .accesslevel command
* Added .gethelp command (pings helpful users in channels)
* Added a converse module
* Added a new reminder system
