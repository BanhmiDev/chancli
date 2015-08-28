#!/usr/bin/env python3
import re
import json
import urwid

from api import Api
from helper import Helper

class State(object):

    def __init__(self):
        # Api calls
        self.api = Api()

        # Save temporary data for quick opening (open <index> command)
        self.current_threads = {'board': None, 'list': []}

        # JSON data
        self.boards_json = None
        self.threads_json = None
        self.thread_json = None
        self.archive_json = None

    def listboards(self):
        # Do not call the API more than once
        if not self.boards_json:
            data = self.api.get_boards()

            # Determine if an error occured
            if not data['error']:
                self.boards_json = data['result']
            else:
                return data['error']

        # Used for urwid.Text which is going to be displayed
        text = [("\nDisplaying all boards. Codes are "), (('highlight'), "highlighted"), ".\n\n"]

        if self.boards_json:
            data = json.loads(self.boards_json)
            for board in data['boards']:
                text.append("/")
                text.append(('highlight', board['board']))
                text.append("/ - {}\n".format(board['title']))

        return {'content': urwid.Text(text), 'status': "Displaying all boards"}

    def open(self, text):
        """Open thread by index shown on the screen."""
        arg = re.match(' \w+$', text[4:])

        if self.current_threads['board'] and arg:
            index = arg.group().strip()

            # Check if convertible to integer
            if index.isdigit():
                index = int(index) - 1 # Indices are incremented by 1
            else:
                index = -1

            # Check if regex matches + index in list
            if arg and -1 < index < len(self.current_threads['list']):
                board = self.current_threads['board']
                thread_id = self.current_threads['list'][index] # Get from the saved thread list
                
                return self.thread("thread {} {}".format(board, thread_id))
            else:
                return {'content': False, 'status': "Invalid argument. Wrong index? Use open <index>."}
        else:
            return {'content': False, 'status': "Open a board first to issue this command."}

    def board(self, text):
        arg1 = re.match(' \w+$', text[5:]) # board <code>
        arg2 = re.match(' \w+ \w+$', text[5:]) # board <code> <page>

        if arg1:
            board = arg1.group().strip()
            page = 1
        elif arg2:
            arg2 = arg2.group().strip()
            arg2 = arg2.split(" ") # Split to get real arguments
            board = arg2[0]
            page = arg2[1]
        else:
            return {'content': False, 'status': "Invalid arguments. Use board <code> or board <code> <page>."}

        data = self.api.get_threads(board, page)

        # Determine if an error occured
        if not data['error']:
            self.threads_json = data['result']
        else:
            return data['error']

        # List containing urwid widgets - to be wrapped up by urwid.Pile
        content = [
            urwid.Text([("\nDisplaying page "), (('highlight'), str(page)), " of /", (('highlight'), str(board)), "/.\n"])
        ]

        if self.threads_json:
            self.current_threads['board'] = board
            del self.current_threads['list'][:] # Reset previous temporary data

            data = json.loads(self.threads_json)
            for index, post in enumerate(data['threads'], 1): # index starting from 1 to open threads without specifying full id (see: open <index>)

                self.current_threads['list'].append(post['posts'][0]['no']) # Quick opening
                _header = [
                    ('highlight', "({}) ".format(index)),
                    ('number', "No. {} ".format(post['posts'][0]['no'])),
                    ('time', "{}".format(post['posts'][0]['now']))
                ]

                # Check for empty comment
                if "com" in post['posts'][0]:
                    _text = Helper.parse_comment(post['posts'][0]['com'])
                else:
                    _text = "- no comment -\n"

                content.append(urwid.Padding(urwid.Text(_header), 'left', left=0))
                content.append(urwid.Padding(urwid.Text(_text), 'left', left=4)) # Indent text content from header

        return {'content': urwid.Pile(content), 'status': "Displaying page {} of /{}/".format(page, board)}

    def thread(self, text):
        """Open thread by specifying board and id."""
        arg = re.match(' \w+ \w+$', text[6:]) # thread <board> <id>

        if arg:
            arg = arg.group().strip()
            arg = arg.split(" ") # Split to get real arguments

            board = arg[0]
            thread_id = arg[1]
        else:
            return {'content': False, 'status': "Invalid arguments. Use thread <board> <id>."}

        data = self.api.get_thread(board, thread_id)

        # Determine if an error occured
        if not data['error']:
            self.thread_json = data['result']
        else:
            return data['error']

        # List containing urwid widgets - to be wrapped up by urwid.Pile
        content = [
            urwid.Text([("\nDisplaying thread "), (('highlight'), str(thread_id)), " in /", (('highlight'), str(board)), "/.\n"])
        ]

        if self.thread_json:
            data = json.loads(self.thread_json)
            for post in data["posts"]:
                _header = [
                    ('number', "No. {} ".format(post['no'])),
                    ('time', "{}".format(post['now']))
                ]

                if "com" in post:
                    _text = Helper.parse_comment(post['com'])
                else:
                    _text = "- no comment -\n"

                content.append(urwid.Padding(urwid.Text(_header), 'left', left=0))
                content.append(urwid.Padding(urwid.Text(_text), 'left', left=4)) # Indent text content from header

        return {'content': urwid.Pile(content), 'status': "Displaying thread {} in /{}/".format(thread_id, board)}

    def archive(self, text):
        arg = re.match(' \w+$', text[7:])

        if arg:
            board = arg.group().strip()
        else:
            return {'content': False, 'status': "Invalid argument. Use archive <code>."}

        data = self.api.get_archive(board)

        # Determine if an error occured
        if not data['error']:
            self.archive_json = data['result']
        else:
            return data['error']

        # Used for urwid.Text which is going to be displayed
        text = [("\nDisplaying archive"), " of /", (('highlight'), str(board)), "/.\n\n"]

        if self.archive_json:
            self.current_threads['board'] = board
            del self.current_threads['list'][:] # Reset previous temporary data

            data = json.loads(self.archive_json)
            for index, thread in enumerate(data, 1): # index starting from 1 to open threads without specifying full id (see: open <index>)
                self.current_threads['list'].append(thread) # Quick opening
                text.append(('highlight', "[{}]".format(index)))
                text.append(" No. {}\n".format(thread))

        return {'content': urwid.Text(text), 'status': "Displaying archive of /{}/".format(board)}

    def empty(self):
        return {'content': False, 'status': "Type help for instructions, exit to quit."}

    def invalid(self, text):
        return {'content': False, 'status': "Invalid command: {}".format(text)}

    @staticmethod
    def splash():
        return urwid.Text([
            ("\n\n    ____ _   _    _    _   _    ____ _     ___\n"
             "   / ___| | | |  / \  | \ | |  / ___| |   |_ _|\n"
             "  | |   | |_| | / _ \ |  \| | | |   | |    | |\n"
             "  | |___|  _  |/ ___ \| |\  | | |___| |___ | |\n"
             "   \____|_| |_/_/   \_\_| \_|  \____|_____|___|\n"
             "        chancli version 0.0.1")
            ])

    @staticmethod
    def help():
        return {
            'content': urwid.Text([
                ('underline', "\nBasic Commands\n\n"),
                ('Chancli utilizes the official 4chan API, which can be found at https://github.com/4chan/4chan-API.\n\n'),
                ('highlight', "listboards"), " - list available boards aside their code\n",
                ('highlight', "open <id>"), " - open a thread from the current window, specified by its index\n",
                ('highlight', "board <code>"), " - display the first page (ex: board g)\n",
                ('highlight', "board <code> <page>"), " - display the nth page starting from 1\n",
                ('highlight', "thread <board> <id>"), " - open a specific thread\n",
                ('highlight', "archive <code>"), " - display archived threads from a board\n\n",
                ('highlight', "help"), " - show this page\n",
                ('highlight', "license"), " - display the license page\n",
                ('highlight', "exit/quit/q"), " - exit the application"
                ]),
            'status': "Help page"
        }

    @staticmethod
    def license():
        return {
            'content': ("\nThe MIT License (MIT)\n\n"
                "Copyright (c) 2015 Son Nguyen <mail@gimu.org>\n\n"
                "Permission is hereby granted, free of charge, to any person obtaining a copy\n"
                "of this software and associated documentation files (the \"Software\"), to deal\n"
                "in the Software without restriction, including without limitation the rights\n"
                "to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n"
                "copies of the Software, and to permit persons to whom the Software is\n"
                "furnished to do so, subject to the following conditions:\n\n"
                "The above copyright notice and this permission notice shall be included in\n"
                "all copies or substantial portions of the Software.\n\n"
                "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n"
                "IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
                "FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
                "AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
                "LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n"
                "OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN\n"
                "THE SOFTWARE."),
            'status': "License page"
        }
