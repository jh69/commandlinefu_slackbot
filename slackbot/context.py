import os
import sys

no_apik_msg = """
No Slack bot API token found. There are 2 ways to accomplish this:
 1) Add it as the environment variable CLFU_SLACKBOT_TOKEN (better)
 2) Paste it directly into the script. (less ideal, but easier)
"""


def get_context():
    # You can manually configure the bot here, or you can configure it from
    # environment variables. We recommend the latter.
    context = {
        "bot_token": "",
        "bot_trigger": "",
        "max_results": 5,
        "worst_possible_rating": 0
    }

    # set context from environment variables
    if context["bot_token"] == "":
        token = os.getenv("CLFU_SLACKBOT_TOKEN")

        if token is None:
            print(no_apik_msg)
            sys.exit(1)

        context["bot_token"] = token

    if context["bot_trigger"] == "":
        context["bot_trigger"] = "clfu"

    return context
