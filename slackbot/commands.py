import time
import base64

from . import commandlinefu
from . import helpers


def parse_slack_output(output=[], context={}):
    if "bot_trigger" not in context:
        return None, None

    trigger = context["bot_trigger"]

    if len(output) > 0:

        for msg in output:

            if "text" not in msg:
                continue

            if msg["text"].startswith(trigger) is False:
                continue

            tmp_output = str(msg["text"].strip().lower())
            olen = len(tmp_output)
            tlen = len(trigger)

            return tmp_output[tlen+1:olen], msg["channel"]

    return None, None


def handle_command(command, channel, slack_client, ctx):
    data = commandlinefu.download(command)
    parsed_data = commandlinefu.parse_response(data, command, ctx)

    slack_client.api_call(
        "chat.postMessage", channel=channel, text=parsed_data, as_user=True)

    print helpers.get_time() + " Someone searched: " + command
