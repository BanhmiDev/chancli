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
        self.convert_charrefs = False
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

class Api(object):

    def parse_comment(self, html):
        """Strip most HTML tags."""
        # Indent comment string
        html = html.replace("<br>", '\n    ')
        html = html.replace("&gt;", '>')
        html = html.replace("&quot;", '"')

        # After preserving some tags, strip all of them
        s = MLStripper()
        s.feed(html)

        return "    " + s.get_data() # Indent first line of comment
    
    def get_threads(self, board, page=1):
        """Return first threads by their first post, board and page."""
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/" + board + "/" + str(page) + ".json").read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return "\nCould not generate thread list\n\nPossible Reasons:\n- invalid board or page\n\n" + str(error)

        if data:
            data = json.loads(data)
            for index, post in enumerate(data["threads"]): # index can be specified to quickly open the thread (see: open <index>)
                result += "\n\n [" + str(index) + "] No. " + str(post["posts"][0]["no"]) + " " + post["posts"][0]["now"] + "\n"
                if "com" in post["posts"][0]: # Check for empty comment
                    result += self.parse_comment(post["posts"][0]["com"])
                else:
                    result += "    ---"

        return result

    def get_thread(self, board, thread_id):
        """Get particular thread by id."""
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/" + board + "/thread/" + str(thread_id) + ".json").read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return "\nCould not generate thread\n\nPossible reasons:\n- invalid board or thread id\n\n" + str(error)

        if data:
            data = json.loads(data)
            for post in data["posts"]:
                result += "\n\nNo. " + str(post["no"]) + " " + post["now"] + "\n"
                if "com" in post: # Check for empty comment
                    result += self.parse_comment(post["com"])
                else:
                    result += "    ---"

        return result

    def get_archive(self, board):
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/" + board + "/archive.json").read().decode("utf-8")
        except urllib.error.HTTPError as error:
            return "\nCould not generate archived thread list\n\nPossible reasons:\n- invalid board\n\n" + str(error)

        if data:
            data = json.loads(data)
            for index, thread in enumerate(data): # index can be specified to quickly open the thread (see: open <index>)
                result += "\n[" + str(index) + "] " + str(thread)

        return result
