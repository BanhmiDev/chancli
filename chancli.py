#!/usr/bin/env python3
from state import State
from urwid import MetaSignals
import urwid
import sys
import re

class MainWindow(object):

    __metaclass__ = MetaSignals
    signals = ["keypress", "quit"]

    _palette = [
        ('divider', 'black', 'light gray'),
        ('text', 'light gray', 'default'),
        ('bold', 'light gray', 'default', 'bold'),
        ('underline', 'light gray', 'default', 'underline'),
        ('body', 'text'),
        ('footer', 'text'),
        ('header', 'text'),
    ]

    def __init__(self, sender="1234567890"):
        self.mark_quit = False
        self.sender = sender

    def main(self):
        """Entry point."""
        self.ui = urwid.raw_display.Screen()
        self.ui.register_palette(self._palette)
        self.build_ui()
        self.ui.run_wrapper(self.run)

    def build_ui(self):
        """Build the urwid UI."""
        self.header = urwid.Text("Chancli")
        self.content = urwid.SimpleListWalker([])
        self.content.append(State.splash_content())
        self.body = urwid.ListBox(self.content)
        self.divider = urwid.Text("Type help for instructions, exit to quit.")
        self.footer = urwid.Edit("> ")

        self.header = urwid.AttrWrap(self.header, "divider")
        self.body = urwid.AttrWrap(self.body, "body")
        self.divider = urwid.AttrWrap(self.divider, "divider")
        self.footer = urwid.AttrWrap(self.footer, "footer")

        self.footer.set_wrap_mode("space")

        main_frame = urwid.Frame(self.body, header=self.header, footer=self.divider)
        
        self.context = urwid.Frame(main_frame, footer=self.footer)
        self.context.set_focus("footer") # Focus on the user input first

    def run(self):
        """Setup and start mainloop."""

        def input_handler(key):
            if self.mark_quit:
                raise urwid.ExitMainLoop
            self.keypress(self.size, key)

        self.size = self.ui.get_cols_rows()

        self.main_loop = urwid.MainLoop(
                self.context,
                screen=self.ui,
                handle_mouse=False,
                unhandled_input=input_handler,
            )

        try:
            self.main_loop.run()
        except KeyboardInterrupt:
            self.quit()

    def print_content(self, text):
        """Print given text as content."""
        # Accept strings, convert them to urwid.Text instances
        if not isinstance(text, urwid.Text):
            text = urwid.Text(text)

        self.content.append(text)

    def parse_input(self):
        """Parse input data."""
        text = self.footer.get_edit_text()

        # Remove input after submitting
        self.footer.set_edit_text("")

        # input: description
        # -------------------------------------------------------------
        # exit, quit, q: exit the application
        # help: show help page
        # license: show license page
        # thread: open specific thread
        # board: trigger either "board <code>" or "board <code> <page>"
        # archive: trigger "archive <code>"
        # empty: return to splash screen
        # else: invalid command

        # Todo: sum up command execution in one if clause
        #       remove startwith and check regex only (?)

        del self.content[:] # Remove previous content

        if text in ('exit', 'quit', 'q'):
            self.quit()
        elif text == "help":
            self.print_content(State.help_content())
            self.divider.set_text("Help page")
        elif text == "license":
            self.print_content(State.license_content())
            self.divider.set_text("License page")
        elif text.startswith("thread"):
            arg1 = re.match(' \w+ \w+$', text[6:]) # thread <board> <id>
            
            if arg1:
                arg1 = arg1.group().strip()
                arg1 = arg1.split(" ") # Split to get real arguments
                self.print_content(State.list_thread(arg1[0], arg1[1]))
                self.divider.set_text("Watching thread " + arg1[1] + " in board /" + arg1[0] + "/")
            else:
                self.print_content(State.splash_content())
                self.divider.set_text("Invalid arguments. Use thread <id>.")
        elif text.startswith("board"):
            arg1 = re.match(' \w+$', text[5:]) # board <code>
            arg2 = re.match(' \w+ \w+$', text[5:]) # board <code> <page>

            if arg1:
                self.print_content(State.list_threads(arg1.group().strip(), 1))
                self.divider.set_text("Watching board /" + arg1.group().strip() + "/ page 1")
            elif arg2:
                arg2 = arg2.group().strip()
                arg2= arg2.split(" ") # Split to get real arguments
                self.print_content(State.list_threads(arg2[0], arg2[1]))
                self.divider.set_text("Watching board /" + arg2[0] + "/ page " + arg2[1])
            else:
                self.print_content(State.splash_content())
                self.divider.set_text("Invalid arguments. Use board <code> or board <code> <page>.")
        elif text.startswith("archive"):
            arg1 = re.match(' \w+$', text[5:])
        elif text.strip() == "":
            self.print_content(State.splash_content())
            self.divider.set_text("Type help for instructions, exit to quit.")
        else:
            self.print_content(State.splash_content())
            self.divider.set_text("Invalid command: " + text)

    def keypress(self, size, key):
        """Handle user input."""
        urwid.emit_signal(self, "keypress", size, key)

        # Focus management
        if key == "up" or key == "down":
            self.context.set_focus("body")
        else:
            self.context.set_focus("footer")

        # New dimension on resize
        if key == "window resize":
            self.size = self.ui.get_cols_rows()
        elif key == "enter":
            # Parse input data
            self.parse_input()
        elif key in ("ctrl d", 'ctrl c'):
            # Quit by key combination
            self.quit()

    def quit(self):
        """Quit the application."""
        urwid.emit_signal(self, "quit")
        self.mark_quit = True

        sys.exit(0)

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.main()
