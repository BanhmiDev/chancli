#!/usr/bin/env python3
import re
import urwid

from api import Api

class State(object):

    def __init__(self):
        self.current_threads = [] # Save temporary data
        self.api = Api() # Api calls

    def listboards(self):
        return {'content': self.api.get_boards(), 'status': "Listing boards' information"}

    def open(self, text):
        """Open thread by index shown on the screen."""
        if self.current_threads:
            arg = re.match(' \w+$', text[4:])
            index = arg.group().strip()

            # Check if regex matches + convertible to integer + index in list
            if arg and index.isdigit() and index in self.current_threads['list']:
                index = int(index) - 1 # Indices are incremented by 1
                board = self.current_threads['board']
                thread_id = self.current_threads['list'][index] # Get from the saved thread list
                return {'content': self.list_thread(board, thread_id), 'status': "Watching board /%s/, thread %s" % (board, thread_id)}
            else:
                return {'content': self.splash_content(), 'status': "Invalid argument. Wrong index? Use open <index>."}
        else:
            return {'content': self.splash_content(), 'status': "Open a board first to issue this command."}

    def thread(self, text):
        """Open thread by specifying board and id."""
        arg = re.match(' \w+ \w+$', text[6:]) # thread <board> <id>

        if arg:
            arg = arg.group().strip()
            arg = arg.split(" ") # Split to get real arguments

            result = self.api.get_thread(arg[0], arg[1])
            return {'content': result, 'status': "Watching board /%s/, thread %s" % (arg[0], arg[1])}
        else:
            return {'content': self.splash_content(), 'status': "Invalid arguments. Use thread <board> <id>."}

    def board(self, text):
        arg1 = re.match(' \w+$', text[5:]) # board <code>
        arg2 = re.match(' \w+ \w+$', text[5:]) # board <code> <page>

        if arg1:
            arg1 = arg1.group().strip()
            return {'content': self.list_threads(arg1, 1), 'status': "Watching board /%s/ page 1" % arg1}
        elif arg2:
            arg2 = arg2.group().strip()
            arg2 = arg2.split(" ") # Split to get real arguments
            return {'content': self.list_threads(arg2[0], arg2[1]), 'status': "Watching board /%s/ page %s" % (arg2[0], arg2[1])}
        else:
            return {'content': self.splash_content(), 'status': "Invalid arguments. Use board <code> or board <code> <page>."}

    def empty(self):
        return {'content': self.splash_content(), 'status': "Type help for instructions, exit to quit."}

    def invalid(self, text):
        return {'content': self.splash_content(), 'status': "Invalid command: %s" % text}

    @staticmethod
    def splash_content():
        return urwid.Text([
            ("\n\n    ____ _   _    _    _   _    ____ _     ___\n"
             "   / ___| | | |  / \  | \ | |  / ___| |   |_ _|\n"
             "  | |   | |_| | / _ \ |  \| | | |   | |    | |\n"
             "  | |___|  _  |/ ___ \| |\  | | |___| |___ | |\n"
             "   \____|_| |_/_/   \_\_| \_|  \____|_____|___|\n"
             "        chancli version 0.0.1")
            ])

    def list_thread(self, board, thread_id):
        result = self.api.get_thread(board, thread_id)
        return result

    def list_threads(self, board, page):
        result = self.api.get_threads(board, page)
        self.current_threads = result

        return result['string']

    @staticmethod
    def list_archived_threads(board):
        result = self.api.get_archive(board)
        return result

    @staticmethod
    def help():
        return {
            'content': urwid.Text([
                ('underline', "\nBasic Commands\n\n"),
                ('Chancli utilizes the official 4chan API, which can be found at https://github.com/4chan/4chan-API.\n\n'),
                ('bold', "listboards"), " - list available boards aside their code\n",
                ('bold', "open <id>"), " - open a thread from the current window, specified by its index\n",
                ('bold', "thread <board> <id>"), " - open a specific thread\n",
                ('bold', "board <code>"), " - display the first page (ex: board g)\n",
                ('bold', "board <code> <page>"), " - display the nth page starting from 1\n",
                ('bold', "archive <code>"), " - display archived threads from a board\n\n",
                ('bold', "help"), " - show this page\n",
                ('bold', "license"), " - display the license page\n",
                ('bold', "exit/quit/q"), " - exit the application"
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
