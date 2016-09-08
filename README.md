# CommandlineFu Slackbot
This is a simple slackbot based that fetches search results from commandlinefu.com and displays them in slack.
It is based on the instructions [given here](https://www.fullstackpython.com/blog/build-first-slack-bot-python.html).

## Setup

Navigate to the source directory and install the dependencies with pip:

```bash
pip install -r requirements.txt
```

The slackbot requires a valid slack API token. [This can be accomplished here.](https://my.slack.com/services/new/bot)

You can supply this token either by directly editing `slackbot/core.py`, 
or by setting the environment variable: `CLFU_SLACKBOT_TOKEN` (this is recommended).

### Interacting with the thing
Once the script says it's successfully connected to Slack, check the user list to see if the 
bot is online. If so, invite it to whichever channels you want the bot to work in. Or 
you can just DM the bot directly. Now let's try it, type:

* clfu convert video

**clfu** is the trigger the bot is listening for, and anything that comes after 
it is your search string. You should get back some results for command line 
one-liners related to converting video. Try searching for other stuff too. CLFU is a 
really good repository for cool complicated things you can do from the command line. 
This bot will come in handy for nerds.
