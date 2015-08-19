#!/usr/bin/env python3
import json
import urllib
import urllib.request

from html.parser import HTMLParser

# https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class Api(object):

    def parse_comment(self, html):
        """Strip most HTML tags."""
        html = html.replace("<br>", '\n')
        html = html.replace("&gt;", '>')
        html = html.replace("&quot;", '"')

        # After preserving some tags, strip all of them
        s = MLStripper()
        s.feed(html)
        return s.get_data()
    
    def get_threads(self, board, page=1):
        """Return first threads by their first post, board and page."""
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/" + board + "/" + str(page) + ".json").read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return "Could not generate thread list\n" + str(error)

        if data:
            data = json.loads(data)
            for post in data["threads"]:
                result += str(post["posts"][0]["no"]) + " " + post["posts"][0]["now"] + "\n"
                result += self.parse_comment(post["posts"][0]["com"] + "\n\n")

        return result

    def get_thread(self, id):
        """Get particular thread by id."""
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/" + board + "/thread/" + str(id) + ".json").read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return "Could not generate thread\n" + str(error)

        return result

    def get_archive(self, board):
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/" + board + "/archive.json").read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return "Could not generate thread list\n" + str(error)

        return result
