import urllib
import base64
import requests
import json


def endpoint(command):
    return "http://commandlinefu.com/commands/matching/%s/%s/json" % (
        urllib.quote(command),
        base64.b64encode(command))


def download(command):
    res = requests.get(endpoint(command))

    if res.status_code != 200:
        return "Error contacting CLFU API. (HTTP-%d)" % res.status_code

    return res.text


def parse_response(textdata, command, ctx):
    maxresults = ctx["max_results"]
    min_rating = ctx["worst_possible_rating"]

    postscounter = 0  # number of items we've added to the buffer string
    output = "<%s|*CommandlineFu*> results for *%s*:\n" % (
        "http://www.commandlinefu.com", command)

    try:
        js = json.loads(textdata)
    except ValueError:
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
            if int(i["votes"]) == qual:
                output += "<%s|%s> _(Upvotes: %s)_\n```%s```\n\n" % (
                    i["url"],
                    i["summary"],
                    i["command"],
                    i["votes"])

                postscounter += 1

                # got our max, we're good
                if postscounter == maxresults:
                    return output
        qual -= 1

    # if we get this far and still have nothing to show for it...
    if len(output) < 100:
        tmp_output = "There were results, but none with an upvote rating of "
        tmp_output += "at least " + str(min_rating)

    return output
