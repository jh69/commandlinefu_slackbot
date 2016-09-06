import os
import time
import requests
import json
import base64
import urllib
from slackclient import SlackClient

# =========== User Configurable Stuff ===========

mybottoken = "[Paste API token here]"
clfutrigger = "clfu"  # trigger word that precedes a search
maxresults = 5  # maximum number of results to return on a search
worstpossiblerating = 0  # worst possible upvote count of results to return

# ===============================================

READ_WEBSOCKET_DELAY = 1

if "[Paste" not in mybottoken:  # if user has inserted their bot token...
    apitoken = mybottoken
else:
    apitoken = os.environ.get('CLFU_SLACKBOT_TOKEN')

if apitoken:
    pass
else:
    print """\nNo Slack bot API token found. There are 2 ways to accomplish this:
 1) Add it as the environment variable CLFU_SLACKBOT_TOKEN (better)
 2) Paste it directly into the script. (less ideal, but easier)
 """
    exit()

slack_client = SlackClient(apitoken)


def msgenc(string):
    # these 3 characters must be replaced for posting messages on slack
    return (
        string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    )


def gettime():
    time_str = str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
    return "[" + time_str + "]"


def parseclfujson(textdata, searchstr):
    postscounter = 0  # number of items we've added to the buffer string
    output = "<http://www.commandlinefu.com|*CommandlineFu*> results for **:\n"

    try:
        js = json.loads(textdata)
    except:
        return "There was a problem parsing the json returned from the server."
    if len(js) < 1:
        return "No results. Try again using different search terms."

    # let's find the highest number of votes in the results
    qual = 0
    for i in js:
        if int(i['votes']) > qual:
            qual = int(i['votes'])

    # this loops over the results grabbing the highest vote count first,
    # then drops a quality level, loops again, drops a level, etc
    # which should effectively return best search results at the top
    while qual > 0:
        for i in js:
            if int(i['votes']) == qual:
                url = i["url"]
                summary = i["summary"]
                cmd = i["command"]
                votes = i["votes"]

                output += "<" + url + "|" + summary + ">"
                output += " _(Upvotes: " + votes + ")_\n```" + cmd + "```\n\n"
                postscounter += 1

                # got our max, we're good
                if postscounter == maxresults:
                    return output
        qual -= 1

    # if we get this far and still have nothing to show for it...
    if len(output) < 100:
        tmp_output = "There were results, but none with an upvote rating of "
        tmp_output += "at least " + str(worstpossiblerating)

    return output


def downloadclfujson(url):
    r = requests.get(url)
    if r.status_code != 200:
        return "There was a problem contacting the CLFU api. HTTP code %s" % (
            str(r.status_code))
    return r.text


def handle_command(command, channel):
    fullurl = "http://commandlinefu.com/commands/matching/%s/%s/json" % (
        urllib.quote(command), base64.b64encode(command))

    datafromclfu = downloadclfujson(fullurl)
    parsedjson = parseclfujson(datafromclfu, command)
    response = parsedjson

    slack_client.api_call(
        "chat.postMessage", channel=channel, text=response, as_user=True)

    print gettime() + " Someone searched: " + command


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            otext = output["text"]
            if output and 'text' in output and otext.startswith(clfutrigger):
                tmp_output = otext.strip().lower()
                clfulen = len(clfutrigger)
                return tmp_output[clfulen+1:clfulen], output["channel"]
    return None, None


# main function
def start():
    if slack_client.rtm_connect():
        print(gettime() + " Bot successfully connected to slack, fool.")

        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token?")
