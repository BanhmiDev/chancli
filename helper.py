import re
import urwid
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

class Helper:
    @staticmethod
    def parse_comment(html):
        """Return urwid.Text formatted string."""
        # Replace HTML breaks with \n
        html = html.replace("<br>", '\n')
        html = html.replace("&gt;", '>')
        html = html.replace("&quot;", '"')

        s = MLStripper()
        s.feed(html)
        html = s.get_data()

        html_list = re.split(r'\n', html)

        for index, line in enumerate(html_list):
            html_list[index] += "\n"

            if re.search('>', line): # Green-texting
                html_list[index] = ('quote', line + "\n")

        html_list.insert(0, "\n") # Newline at the beginning
        html_list.append("\n") # Newline at the end

        return html_list
