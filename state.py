#!/usr/bin/env python3
import urwid
from api import Api

class State(object):

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

    @staticmethod
    def list_threads(board, page):
        result = Api().get_threads(board, page)
        return result

    @staticmethod
    def help_content():
        return urwid.Text([
            ('underline', "\nBasic Commands\n\n"),
            ('Chancli utilizes the official 4chan API, which can be found at https://github.com/4chan/4chan-API.\n\n'),
            ('bold', "listboards"), " - list available boards aside their code\n",
            ('bold', "board <code>"), " - display the first page (ex: board g)\n",
            ('bold', "board <code> <page>"), " - display the nth page starting from 1\n",
            ('bold', "archive <code>"), " - display archived threads from a board\n\n",
            ('bold', "help"), " - show this page\n",
            ('bold', "license"), " - display the license page\n",
            ('bold', "exit/quit/q"), " - exit the application"


            ])

    @staticmethod
    def license_content():
        return urwid.Text([
            ("\nThe MIT License (MIT)\n\n"
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
             "THE SOFTWARE.")
            ]) 

