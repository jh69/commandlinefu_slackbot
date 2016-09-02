import os
import time
import requests
import json
import base64
import urllib
from slackclient import SlackClient

#=========== User Configurable Stuff ===========

mybottoken = "[Paste API token here]"
clfutrigger = "clfu" #trigger word that precedes a search
maxresults = 5 #maximum number of results to return on a search
worstpossiblerating = 0 #worst possible upvote count of results to return

#===============================================

if "[Paste" not in mybottoken: #if user has inserted their bot token...
 	apitoken = mybottoken
else:
	apitoken = os.environ.get('CLFU_SLACKBOT_TOKEN')

if apitoken:
	pass
else:
	print """\nNo Slack bot API token found. There are 2 ways to accomplish this:
 1) Add it as the environment variable CLFU_SLACKBOT_TOKEN (better)
 2) Paste it directly into the script. (less ideal, but easier)"""
	exit()

slack_client = SlackClient(apitoken)

def msgenc(string):
	#these 3 characters must be replaced for posting messages on slack
	return string.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def gettime():
	return "[" + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())) + "]"

def parseclfujson(textdata, searchstr):
	postscounter = 0 #number of items we've added to the buffer string
	stringtoprint = "<http://www.commandlinefu.com|*CommandlineFu*> results for *" + \
		searchstr + "*:\n"
	try:
		js = json.loads(textdata)
	except:
		return "There was a problem parsing the json returned from the server."
	if len(js) < 1: return "No results. Try again using different search terms."

	#let's find the highest number of votes in the results
	qual = 0
	for i in js:
		if int(i['votes']) > qual:
			qual = int(i['votes'])

	#this loops over the results grabbing the highest vote count first,
	#then drops a quality level, loops again, drops a level, etc
	#which should effectively return best search results at the top
	while qual > 0:
		for i in js:
			if int(i['votes']) == qual:
				stringtoprint = stringtoprint + "<" + i['url'] + "|" + \
					msgenc(i['summary']) + "> _(Upvotes: " + i['votes'] + ")_\n```" + \
					msgenc(i['command']) + "```\n\n"
				postscounter += 1
				if postscounter == maxresults: return stringtoprint #got our max, we're good
		qual -= 1

	if len(stringtoprint) < 100: #if we get this far and still have nothing to show for it...
		return "There were results, but none with an upvote rating of at least " + \
			str(worstpossiblerating) + "."

	return stringtoprint


def downloadclfujson(url):
	r = requests.get(url)
	if r.status_code != 200:
		return "There was a problem contacting the CLFU api. HTTP code " + str(r.status_code)
	return r.text

def handle_command(command, channel):
	fullurl = "http://commandlinefu.com/commands/matching/" + \
		urllib.quote(command) + "/" + base64.b64encode(command) + "/json"
	datafromclfu = downloadclfujson(fullurl)
	parsedjson = parseclfujson(datafromclfu, command)
	response = parsedjson
	slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
	print gettime() + " Someone searched: " + command


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['text'].startswith(clfutrigger):
                return output['text'].strip().lower()[len(clfutrigger)+1:len(output['text'])], output['channel']
				#this returns message text and channel
    return None, None


if __name__ == "__main__":
	print gettime() + " Started"
	READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
	if slack_client.rtm_connect():
		print gettime() + " Bot successfully connected to slack, fool."
		while True:
			command, channel = parse_slack_output(slack_client.rtm_read())
			if command and channel:
				handle_command(command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print("Connection failed. Invalid Slack token?")
