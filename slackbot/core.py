import time

from slackclient import SlackClient
from . import context
from . import commands
from . import helpers


def start(websocket_delay=1):
    ctx = context.get_context()
    slack_client = SlackClient(ctx["bot_token"])

    if slack_client.rtm_connect():
        print("%s Bot successfully connected to slack, fool." % (
            helpers.get_time()))

        while True:
            output = slack_client.rtm_read()
            command, channel = commands.parse_slack_output(output, ctx)

            if command and channel:
                commands.handle_command(command, channel, slack_client, ctx)

            time.sleep(websocket_delay)
    else:
        print("Connection failed. Invalid Slack token?")
