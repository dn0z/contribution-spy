#!/usr/bin/env python

import datetime
import os.path
import time

from HTMLParser import HTMLParser
from requests import get

URL = "https://github.com/users/%s/contributions"
log_file = "contributions.csv"


class CustomHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rects = []

    def handle_starttag(self, tag, attrs):
        if tag == "rect":
            self.rects.append(attrs)


# noinspection SpellCheckingInspection
def main():
    # Get username to check from file
    with open("usernames.txt") as f:
        username = f.readline()

    # If username has length 0, do not run
    if len(username) == 0:
        return

    while True:
        # Get number of contributions
        r = get(URL % username)
        parser = CustomHTMLParser()
        parser.feed(r.text)
        d = dict(parser.rects[-1])

        number = d["data-count"]
        date = d["data-date"]

        current_date = datetime.datetime.now()

        # If log file does not exist, write headers to it
        if not os.path.isfile(log_file):
            # Create log file with headers
            with open(log_file, "w") as f:
                f.write("curr_time,ghb_date,contribs\n")

        # Write to log file
        with open(log_file, "a") as f:
            f.write(str(current_date) + "," + date + "," + str(number) + "\n")
            # print(str(current_date) + "," + date + "," + str(number) + "\n")

        # Wait five minutes
        time.sleep(5)


if __name__ == '__main__':
    main()
