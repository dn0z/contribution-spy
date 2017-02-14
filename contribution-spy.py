#!/usr/bin/env python

import datetime
import os.path
import time
from random import randint

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

    contribs_prev = None

    while True:
        # Get number of contributions
        r = get(URL % username)
        parser = CustomHTMLParser()
        parser.feed(r.text)
        d = dict(parser.rects[-1])

        number = int(d["data-count"])
        date = d["data-date"]

        # If this is the 1st loop, set the previous contributions to current
        if contribs_prev is None:
            contribs_prev = number

        # Get current time and difference of contributions
        current_date = datetime.datetime.now()
        contribs_diff = number - contribs_prev

        # If log file does not exist, create it with headers
        if not os.path.isfile(log_file):
            # Create log file with headers
            with open(log_file, "w") as f:
                f.write("curr_time,ghb_date,contribs,diff\n")

        # Write to log file if there was a change in contributions
        if contribs_diff > 0:
            with open(log_file, "a") as f:
                f.write(str(current_date) + "," + date + "," + str(number) +
                        "," + str(contribs_diff) + "\n")

            # Save new "previous" number of contributions
            contribs_prev = number

            # Print change to console
            print(str(current_date) + " -> There was a change of: " +
                  str(contribs_diff) + " contributions!")

        # Wait 150-500 seconds at random to simulate superhuman behavior
        wait_time = randint(150, 500)
        time.sleep(wait_time)


if __name__ == '__main__':
    main()
