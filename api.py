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

class ApiError(object):

    @staticmethod
    def get_error(target, error):
        """Return error message."""
        return "\nCould not generate {}\nFull error code: {}".format(target, error)

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

    def get_boards(self):
        """Return boards' information."""
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/boards.json").read().decode('utf-8')
        except urllib.error.HTTPError as error:
            return ApiError.get_error("boards list", error)
        except urllib.error.URLError as error:
            return ApiError.get_error("boards list", error)

        if data:
            data = json.loads(data)
            for board in data['boards']:
                result += "/{}/ - {}\n".format(board['board'], board['title'])

        return result
    
    def get_threads(self, board, page=1):
        """Return a dict containing:
        the board, a list of thread IDs, a string to render from
        """
        data = None
        result = {'board': board, 'list': [], 'string': ''}

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/{}/{}.json".format(board, page)).read().decode('utf-8')
        except urllib.error.HTTPError as error:
            result['string'] = ApiError.get_error("threads list", error)
            return result
        except urllib.error.URLError as error:
            result['string'] = ApiError.get_error("threads list", error)
            return result

        if data:
            data = json.loads(data)
            for index, post in enumerate(data['threads'], 1): # index starting from 1 to open threads without specifying full id (see: open <index>)
                result['list'].append(post['posts'][0]['no'])
                result['string'] += "\n\n[{}] No. {} {}\n".format(index, post['posts'][0]['no'], post['posts'][0]['now'])
                if "com" in post['posts'][0]: # Check for empty comment
                    result['string'] += self.parse_comment(post['posts'][0]['com'])
                else:
                    result['string'] += "    ---"

        return result

    def get_thread(self, board, thread_id):
        """Get particular thread by id."""
        data = None
        result = ""

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/{}/thread/{}.json".format(board, thread_id)).read().decode('utf-8')
        except urllib.error.HTTPError as error:
            return ApiError.get_error("thread list", error)
        except urllib.error.URLError as error:
            return ApiError.get_error("thread list", error)

        if data:
            data = json.loads(data)
            for post in data["posts"]:
                result += "\n\nNo. {} {}\n".format(post['no'], post['now'])
                if "com" in post: # Check for empty comment
                    result += self.parse_comment(post['com'])
                else:
                    result += "    ---"

        return result

    def get_archive(self, board):
        """Return a dict containing:
        the board, a list of thread IDs, a string to render from
        """
        data = None
        result = {'board': board, 'list': [], 'string': ''}

        try:
            data = urllib.request.urlopen("https://a.4cdn.org/{}/archive.json".format(board)).read().decode('utf-8')
        except urllib.error.HTTPError as error:
            result['string'] = ApiError.get_error("archive list", error)
            return result
        except urllib.error.URLError as error:
            result['string'] = ApiError.get_error("archive list", error)
            return result

        if data:
            data = json.loads(data)
            for index, thread in enumerate(data, 1): # index starting from 1 to open threads without specifying full id (see: open <index>)
                result['list'].append(thread)
                result['string'] += "\n[{}] {}".format(index, thread)

        return result
