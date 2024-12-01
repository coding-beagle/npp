import click
from pathlib import Path
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
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
    text_field: Window
    title: str

    def __init__(self):

        self.title = ""

        self.buffer1 = Buffer()
        self.text_field = Window(content=BufferControl(
            buffer=self.buffer1), height=Dimension(max=10))

        self.update_ui()

        self.app = Application(layout=self.layout, full_screen=True,
                               key_bindings=kb, style=style)

    def update_ui(self):
        self.root_container = HSplit([
            Window(content=FormattedTextControl(text=self.title),
                   style='bg:#7b39cc fg:#ffffff bold',
                   height=Dimension(max=1)),
            self.text_field]
        )
        self.layout = Layout(self.root_container)
        self.app = Application(layout=self.layout, full_screen=True,
                               key_bindings=kb, style=style)
        self.app.invalidate()

    def pop_up(self, str, colour, yes_cb, no_cb):
        self.pop_up_enabled = True

        @kb.add('y', filter=is_pop_up)
        def yes_handler(buffer):
            yes_cb()
            self.pop_up_enabled = False

        @kb.add('n', filter=is_pop_up)
        def no_handler(buffer):
            no_cb()
            self.pop_up_enabled = False

        yes_no_window = Window(
            content=FormattedTextControl(text=str),
            style=f'bg:{colour} fg:#ffffff bold',
            height=Dimension(max=1)
        )

        self.root_container = HSplit([
            Window(content=FormattedTextControl(text=self.title),
                   style='bg:#7b39cc fg:#ffffff bold',
                   height=Dimension(max=1)),
            self.text_field,
            yes_no_window],
        )
        # self.update_ui()
        self.layout = Layout(self.root_container)
        self.app.layout = self.layout
        self.app.invalidate()

    def add_text_to_content(self, text):
        self.buffer1.insert_text(text)

    def set_title(self, title):
        self.title = title
        self.update_ui()
        self.app.invalidate()

    def run(self):
        self.app.run()


@ kb.add('c-x')
def exit_(event):
    event.app.exit()


@ kb.add('c-o')
def write_out_(event):
    editor.pop_up("Write out file?", "#ffccff", yes_cb=lambda: print(
        "yes"), no_cb=lambda: print("no"))


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
