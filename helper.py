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
        """Strip most HTML tags."""
        # Indent comment string
        html = html.replace("<br>", '\n    ')
        html = html.replace("&gt;", '>')
        html = html.replace("&quot;", '"')

        # After preserving some tags, strip all of them
        s = MLStripper()
        s.feed(html)

        # Indent first line of comment, add newline at the end
        return "    " + s.get_data() + "\n\n"
