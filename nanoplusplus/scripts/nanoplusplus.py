import click
from pathlib import Path
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout import ScrollablePane, ScrollOffsets
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition

kb = KeyBindings()

style = Style([
    ('top', 'bg:#5b29bc fg:#ffffff bold')
])


@Condition
def is_pop_up():
    return editor.pop_up_enabled


class Editor():
    app: Application
    layout: Layout
    root_container: HSplit
    text_window: Window
    title: str
    pop_up_enabled: bool

    def __init__(self):

        self.title = ""

        self.pop_up_enabled = False

        self.buffer1 = Buffer()
        self.text_window = Window(content=BufferControl(
            buffer=self.buffer1))
        self.text_scroll = ScrollablePane(
            self.text_window, show_scrollbar=False)

        self.update_ui()

        self.app = Application(layout=self.layout, full_screen=True,
                               key_bindings=kb, style=style)

    def update_ui(self):
        self.root_container = HSplit([
            Window(content=FormattedTextControl(text=self.title),
                   style='bg:#7b39cc fg:#ffffff bold',
                   height=Dimension(max=1)),
            self.text_scroll]
        )
        self.layout = Layout(self.root_container)
        self.app = Application(layout=self.layout, full_screen=True,
                               key_bindings=kb, style=style)
        self.app.invalidate()

    def pop_up(self, str, colour, yes_cb=None, no_cb=None):
        if (self.pop_up_enabled):
            return

        self.pop_up_enabled = True

        @kb.add('y', filter=is_pop_up)
        def yes_handler(buffer):
            if (yes_cb is not None):
                yes_cb()
            self.pop_up_enabled = False
            self.root_container = HSplit([
                Window(content=FormattedTextControl(text=self.title),
                       style='bg:#7b39cc fg:#ffffff bold',
                       height=Dimension(max=1)),
                self.text_scroll,],
            )
            self.layout = Layout(self.root_container)
            self.app.layout = self.layout
            self.app.invalidate()

        @kb.add('n', filter=is_pop_up)
        def no_handler(buffer):
            if (no_cb is not None):
                no_cb()
            self.pop_up_enabled = False
            self.root_container = HSplit([
                Window(content=FormattedTextControl(text=self.title),
                       style='bg:#7b39cc fg:#ffffff bold',
                       height=Dimension(max=1)),
                self.text_scroll,],
            )
            self.layout = Layout(self.root_container)
            self.app.layout = self.layout
            self.app.invalidate()

        yes_no_window = Window(
            content=FormattedTextControl(text=str),
            style=f'bg:{colour} fg:#ffffff bold',
            height=Dimension(max=1)
        )

        self.root_container = HSplit([
            Window(content=FormattedTextControl(text=self.title),
                   style='bg:#7b39cc fg:#ffffff bold',
                   height=Dimension(max=1)),
            self.text_scroll,
            yes_no_window],
        )
        self.layout = Layout(self.root_container)
        self.app.layout = self.layout
        self.app.invalidate()

    def add_text_to_content(self, text):
        self.buffer1.insert_text(text)
        self.buffer1.cursor_position = 0

    def set_title(self, title):
        self.title = title
        self.update_ui()
        self.app.invalidate()

    def run(self):
        self.app.run()


@ kb.add('c-z')
def exit_(event):
    editor.pop_up("Exit from file? (y/n)", "#00ccff",
                  yes_cb=event.app.exit)


@ kb.add('c-o')
def write_out_(event):
    editor.pop_up("Write out file? (y/n)", "#ffccff", no_cb=event.app.exit)


@ click.command()
@ click.argument('filename', required=False)
def cli(filename: str) -> int:
    """Open a file in the NanoPlusPlus text editor!"""
    # try:
    if (filename is None):
        filename = ""
    target = Path(filename)

    if (target.exists() and filename != ""):
        editor.set_title(f"Editing {filename}")
        with open(target, "r") as fp:
            content = fp.read()
            editor.add_text_to_content(content)
    else:
        editor.set_title(f"New Buffer")

    editor.run()


editor = Editor()
