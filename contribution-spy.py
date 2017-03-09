#!/usr/bin/env python

import datetime
import time
import json
import sys
import os
from random import randint

from html.parser import HTMLParser
from requests import get, exceptions
from pushover import Client


# noinspection SpellCheckingInspection
class CustomHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rects = []

    def handle_starttag(self, tag, attrs):
        if tag == "rect":
            self.rects.append(attrs)


class ExternalData(object):
    def __init__(self):
        cd = os.path.join(os.getcwd(), os.path.dirname(__file__))
        __location__ = os.path.realpath(cd)

        # Read `config.json`
        json_contents = self.get_local_json_contents(
            os.path.join(__location__, "config.json"))

        # Make sure it contains the required properties
        if json_contents["username"] is None:
            raise ValueError("GitHub username is not set")
        if json_contents["logFile"] is None:
            raise ValueError("Log file is not set")
        if json_contents["pushoverUserKey"] is None:
            raise ValueError("Pushover user key is not set")
        if json_contents["pushoverApiToken"] is None:
            raise ValueError("Pushover API token is not set")

        self.username = json_contents["username"]
        self.log_file = json_contents["logFile"]
        self.user_key = json_contents["pushoverUserKey"]
        self.api_token = json_contents["pushoverApiToken"]

    @staticmethod
    def get_local_json_contents(path_to_json):
        try:
            with open(path_to_json) as json_file:
                try:
                    data = json.load(json_file)
                except ValueError:
                    print("Invalid JSON")
                    raise
        except IOError:
            print("An error occurred while reading the JSON file")
            raise

        return data


def wait_random():
    # Wait 150-500 seconds at random to simulate superhuman behavior
    wait_time = randint(150, 500)
    time.sleep(wait_time)


# noinspection SpellCheckingInspection
def main():
    # Load the external data
    external = ExternalData()

    # Check the argument to determine whether we are going to send push notifications
    client = None
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["true", "yes", "y"]:
            client = Client(external.user_key, api_token=external.api_token)

    # If username has length 0, do not run
    if len(external.username) == 0:
        print("Username is empty")
        return

    contribs_prev = None
    date_prev = None

    print("Spying on " + external.username)

    while True:
        # Get number of contributions
        URL = "https://github.com/users/%s/contributions"
        r = None

        try:
            r = get(URL % (external.username.strip()))
        except exceptions.RequestException as e:
            print(e)

        if r is None:
            wait_random()
            continue

        parser = CustomHTMLParser()
        parser.feed(r.text)
        d = dict(parser.rects[-1])

        number = int(d["data-count"])
        date = d["data-date"]

        # If this is the 1st loop, set the previous contributions to current
        if contribs_prev is None or date_prev is None:
            contribs_prev = number
            date_prev = date
        elif date != date_prev:
            # The date changed, reset the number of contributions
            contribs_prev = 0
            date_prev = date

        # Get current time and difference of contributions
        current_date = datetime.datetime.now()
        contribs_diff = number - contribs_prev

        # If log file does not exist, create it with headers
        if not os.path.isfile(external.log_file):
            # Create log file with headers
            try:
                with open(external.log_file, "w") as f:
                    f.write("curr_time,ghb_date,contribs,diff\n")
            except IOError:
                print("Could not create the log file with headers")
                raise

        # Check if there was a change in contributions
        if contribs_diff > 0:
            # Send push notification
            if client is not None:
                msg_base = str(contribs_diff) + " contributions" if contribs_diff > 1 else "a contribution"
                client.send_message(external.username + " made " + msg_base,
                                    title="New contribution")

            # Write to log file
            try:
                with open(external.log_file, "a") as f:
                    f.write(str(current_date) + "," + date + "," + str(number) +
                            "," + str(contribs_diff) + "\n")
            except IOError:
                print("Could not write to log file")

            # Save new "previous" number of contributions
            contribs_prev = number

            # Print change to console
            print(str(current_date) + " -> There was a change of: " +
                  str(contribs_diff) + " contributions!")

        wait_random()


if __name__ == '__main__':
    main()
