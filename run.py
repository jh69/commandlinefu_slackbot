#!/usr/bin/env python

import getopt
import sys

from slackbot import core

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["websocket-delay="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    websocket_delay = 1

    for o, a in opts:
        if o == "--websocket-delay":
            websocket_delay = int(a)
        else:
            print("unhandled argument")
            sys.exit(2)

    core.start(websocket_delay)

if __name__ == "__main__":
    main()
