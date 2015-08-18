#!/usr/bin/env python3
from state import State
from urwid import MetaSignals
import urwid
import sys

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
        self.generic_output_walker = urwid.SimpleListWalker([])
        self.generic_output_walker.append(State.splash_content())
        self.body = urwid.ListBox(self.generic_output_walker)
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

    def print_out(self, text):
        """Print given text as content."""
        # Accept strings, convert them to urwid.Text instances
        if not isinstance(text, urwid.Text):
            text = urwid.Text(text)

        self.generic_output_walker.append(text)

    def keypress(self, size, key):
        """Handle user input."""
        urwid.emit_signal(self, "keypress", size, key)

        # New dimension on resize
        if key == "window resize":
            self.size = self.ui.get_cols_rows()
        elif key == "enter":
            # Parse input data
            text = self.footer.get_edit_text()

            # Remove input after submitting
            self.footer.set_edit_text("")

            if text in ('exit', 'quit', 'q'):
                self.quit()
            elif text == "help":
                del self.generic_output_walker[:]

                self.print_out(State.help_content())
                self.divider.set_text("Help page")
            elif text == "license":
                del self.generic_output_walker[:]

                self.print_out(State.license_content())
                self.divider.set_text("License page")
            elif text.strip() == "":
                # Empty input, return to splash screen
                del self.generic_output_walker[:]

                self.print_out(State.splash_content())
                self.divider.set_text("Type help for instructions, exit to quit.")
            else:
                self.divider.set_text("Invalid command: " + text)
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
