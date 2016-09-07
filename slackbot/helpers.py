import time


def msgenc(string):
    # these 3 characters must be replaced for posting messages on slack
    return (
        string.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))


def get_time():
    return "[%s]" % (
        str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())))
