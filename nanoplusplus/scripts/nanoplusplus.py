import click
from pathlib import Path
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout

kb = KeyBindings()


@kb.add('c-x')
def exit_(event):
    event.app.exit()


@click.command()
@click.argument('filename', required=False)
def cli(filename: str) -> int:
    """Open a file in the NanoPlusPlus text editor!"""
    # try:
    target = Path(filename)
    if (target.exists()):
        buffer1 = Buffer()
        text_field = Window(content=BufferControl(buffer=buffer1))

        root_container = HSplit([
            Window(content=FormattedTextControl(text=f"Editing {filename}")),
            text_field]
        )
        layout = Layout(root_container)
        app = Application(layout=layout, full_screen=True, key_bindings=kb)

        with open(target, "r") as fp:
            content = fp.read()
            buffer1.insert_text(content)

        app.run()

    # except Exception as e:
    #     print(e)
    #     target = None
