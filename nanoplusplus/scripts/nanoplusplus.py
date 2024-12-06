import click
from pathlib import Path
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window, VSplit
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout import ScrollablePane, ScrollOffsets
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.styles import Style
from prompt_toolkit.filters import Condition
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.clipboard import Clipboard

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
    file_name: str

    def __init__(self):

        self.title = ""

        self.pop_up_enabled = False

        self.clipboard = PyperclipClipboard()

        self.buffer1 = Buffer()
        self.text_window = Window(content=BufferControl(
            buffer=self.buffer1))
        self.text_scroll = ScrollablePane(
            self.text_window, show_scrollbar=False)

        self.update_ui()

        self.app = Application(layout=self.layout, full_screen=True,
                               key_bindings=kb, style=style, clipboard=self.clipboard)

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

    def pop_up_confirm(self, str, colour, yes_cb=None, no_cb=None):
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
            self.layout.focus(self.text_scroll)
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

    def pop_up_text_field(self, buffer_prefix, colour, yes_cb=None, no_cb=None, prefill="", call_cb_with_buffer=False):
        if (self.pop_up_enabled):
            return

        self.pop_up_enabled = True

        @kb.add('enter', filter=is_pop_up)
        def yes_handler(buffer):

            self.root_container = HSplit([
                Window(content=FormattedTextControl(text=self.title),
                       style='bg:#7b39cc fg:#ffffff bold',
                       height=Dimension(max=1)),
                self.text_scroll,],
            )
            self.layout = Layout(self.root_container)
            self.app.layout = self.layout
            self.app.layout.focus(self.text_scroll)
            self.pop_up_enabled = False
            self.app.invalidate()
            if (yes_cb is not None):
                if (call_cb_with_buffer):
                    yes_cb(text_buffer.text)
                else:
                    yes_cb()
                self.pop_up_enabled = False

        @kb.add('c-c', filter=is_pop_up)
        def no_handler(buffer):
            if (no_cb is not None):
                no_cb()
            self.root_container = HSplit([
                Window(content=FormattedTextControl(text=self.title),
                       style='bg:#7b39cc fg:#ffffff bold',
                       height=Dimension(max=1)),
                self.text_scroll,],
            )
            self.layout = Layout(self.root_container)
            self.app.layout = self.layout
            self.app.layout.focus(self.text_scroll)
            self.app.invalidate()
            self.pop_up_enabled = False

        text_buffer = Buffer()

        entry_window = Window(
            content=BufferControl(buffer=text_buffer),
            style=f'bg:{colour} fg:#ffffff bold',
            height=Dimension(max=1)
        )

        if (prefill != ""):
            text_buffer.insert_text(prefill)
            text_buffer.cursor_position = len(prefill)

        prefix_window = Window(
            content=FormattedTextControl(text=buffer_prefix),
            style=f'bg:{colour} fg:#ffffff bold',
            height=Dimension(max=1),
            width=Dimension(min=len(buffer_prefix), max=len(buffer_prefix))
        )

        self.root_container = HSplit([
            Window(content=FormattedTextControl(text=self.title),
                   style='bg:#7b39cc fg:#ffffff bold',
                   height=Dimension(max=1)),
            self.text_scroll,
            VSplit([prefix_window, entry_window])],
        )

        self.layout = Layout(self.root_container)
        self.app.layout = self.layout
        self.layout.focus(entry_window)
        self.app.invalidate()

    def pop_up_text(self, text, colour):
        text_window = Window(
            FormattedTextControl(text=text),
            style=f'bg:{colour} fg:#ffffff bold',
            height=Dimension(max=1),
        )
        self.app.invalidate()
        self.root_container = HSplit([
            Window(content=FormattedTextControl(text=self.title),
                   style='bg:#7b39cc fg:#ffffff bold',
                   height=Dimension(max=1)),
            self.text_scroll,
            # Spacer to push text_window up
            Window(height=Dimension(weight=1)),
            text_window],
        )

        self.layout = Layout(self.root_container)
        self.app.layout = self.layout
        self.layout.focus(self.text_scroll)
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


@ kb.add('c-z', filter=~is_pop_up)
def exit_(event):
    editor.pop_up_confirm("Exit from file? (y/n)", "#00ccff",
                          yes_cb=event.app.exit)


def save_file(text: str):
    with open(text, "w") as fp:
        fp.write(editor.buffer1.text)

    editor.pop_up_text(f"{text} saved!", "#00ff00")


@kb.add('c-c', filter=~is_pop_up)
def copy_to_clipboard(event):
    data = editor.buffer1.copy_selection()
    editor.clipboard.set_data(data)
    editor.pop_up_text("Copied to clipboard!", "#00ff00")


@kb.add('c-v', filter=~is_pop_up)
def paste_from_clipboard(event):
    data = editor.clipboard.get_data()
    editor.buffer1.insert_text(data.text)
    editor.pop_up_text("Pasted from clipboard!", "#00ff00")


@ kb.add('c-o')
def write_out_(event, filter=~is_pop_up):
    file_name = ""
    if (hasattr(editor, "file_name")):
        file_name = editor.file_name
    else:
        file_name = ""
    editor.pop_up_text_field("File name: ",
                             "#ffccff", prefill=file_name, yes_cb=save_file, call_cb_with_buffer=True)


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
        editor.file_name = filename
        with open(target, "r") as fp:
            content = fp.read()
            editor.add_text_to_content(content)
    elif (filename != ""):
        editor.set_title(f"New Buffer: {filename}")
        editor.file_name = filename
    else:
        editor.set_title("New Buffer")

    editor.run()


editor = Editor()
