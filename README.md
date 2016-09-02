# CommandlineFu Slackbot
This is a real damn basic slackbot for commandlinefu.com originally based upon the basic writeup here because I'm dull as a board and they explained it to me in a way I could understand https://www.fullstackpython.com/blog/build-first-slack-bot-python.html

It requires the **slackclient** and **requests** packages. Here's how to install them with pip:

* pip install slackclient
* pip install requests

## Usage
First, you must create a bot user under your Slack team settings page here: https://my.slack.com/services/new/bot

Name the bot whatever you want (something like "clfu" would make sense), and add a photo if you like. Make a note of the **API token**-- you'll need it.

### Adding the API token
You can do this in one of two ways. It's probably best to add it as an environment variable (CLFU_SLACKBOT_TOKEN). If you don't know what that is or how to do it for your particular OS, you can also paste it into the script directly on like line 10 or 11 or whatever. It's in there, just look for it.

### Interacting with the thing
Once the script says it's successfully connected to Slack, check the user list to see if the bot is online. If so, invite it to whichever channels you want the bot to work in. Or you can just DM the bot directly. Now let's try it, type:

* clfu convert video

**clfu** is the trigger the bot is listening for, and anything that comes after it is your search string. You should get back some results for command line one-liners related to converting video. Try searching for other stuff too. CLFU is a really good repository for cool complicated things you can do from the command line. This bot will come in handy for nerds.
