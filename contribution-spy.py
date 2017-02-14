#!/usr/bin/env python

from HTMLParser import HTMLParser
from requests import get

URL = "https://github.com/users/%s/contributions"
log_file = "contributions.log"


class CustomHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.rects = []

    def handle_starttag(self, tag, attrs):
        if tag == "rect":
            self.rects.append(attrs)


def main():
    # Get username to check from file
    with open("usernames.txt") as f:
        username = f.readline()

    r = get(URL % username)
    parser = CustomHTMLParser()
    parser.feed(r.text)
    d = dict(parser.rects[-1])

    number = d["data-count"]
    date = d["data-date"]

    print(number)


if __name__ == '__main__':
    main()
