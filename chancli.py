#!/usr/bin/env python3
import sys
import urwid
from urwid import MetaSignals

from state import State

class MainWindow(object):

    __metaclass__ = MetaSignals
    signals = ["keypress", "quit"]

    _palette = [
        ('divider', 'black', 'light gray'),
        ('text', 'white', 'default'),

        ('number', 'dark green', 'default'),
        ('time', 'dark gray', 'default'),
        ('quote', 'light green', 'default'),

        ('highlight', 'yellow', 'default'),
        ('underline', 'yellow', 'default', 'underline'),
        ('bold', 'yellow', 'default', 'bold'),
        ('body', 'text'),
        ('footer', 'text'),
        ('header', 'text'),
    ]

    def __init__(self, sender="1234567890"):
        self.mark_quit = False
        self.sender = sender

        self.state = State()

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
        self.content.append(self.state.splash())
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
                unhandled_input=input_handler
        )

        # Disable bold on bright fonts
        self.main_loop.screen.set_terminal_properties(bright_is_bold=False)

        try:
            self.main_loop.run()
        except KeyboardInterrupt:
            self.quit()

    def print_content(self, text):
        """Print given text as content."""
        # Accept strings, convert them to urwid.Text instances
        if not isinstance(text, (urwid.Text, urwid.Pile)):
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
        # listboards: list all available boards
        # open: open specific thread by index (shown on the screen)
        # thread: open specific thread
        # board: trigger either "board <code>" or "board <code> <page>"
        # archive: trigger "archive <code>"
        # empty: show initial status message
        # else: invalid command

        if text in ("exit", "quit", "q"):
            self.quit()
        elif text == "help":
            _content = self.state.help()
        elif text == "license":
            _content = self.state.license()
        elif text == "listboards":
            _content = self.state.listboards()
        elif text.startswith("open"):
            _content = self.state.open(text)
        elif text.startswith("thread"):
            _content = self.state.thread(text)
        elif text.startswith("board"):
            _content = self.state.board(text)
        elif text.startswith("archive"): # archive <board>
            _content = self.state.archive(text)
        elif text.strip() == "":
            _content = self.state.empty()
        else:
            _content = self.state.invalid(text)

        if _content['content']: # Only update if content given
            del self.content[:] # Remove previous content
            self.print_content(_content['content'])
        self.divider.set_text(_content['status'])

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
        elif key in ("ctrl d", "ctrl c"):
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
