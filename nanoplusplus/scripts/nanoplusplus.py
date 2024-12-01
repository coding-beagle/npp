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

kb = KeyBindings()

style = Style([
    ('top', 'bg:#5b29bc fg:#ffffff bold')
])


@kb.add('c-x')
def exit_(event):
    event.app.exit()


@click.command()
@click.argument('filename', required=False)
def cli(filename: str) -> int:
    """Open a file in the NanoPlusPlus text editor!"""
    # try:
    if (filename is None):
        filename = ""
    target = Path(filename)

    buffer1 = Buffer()
    text_field = Window(content=BufferControl(buffer=buffer1))

    if (target.exists() and filename != ""):
        title = f"Editing {filename}"
        with open(target, "r") as fp:
            content = fp.read()
            buffer1.insert_text(content)
    else:
        title = f"New Buffer"

    root_container = HSplit([
        Window(content=FormattedTextControl(text=title),
               style='bg:#7b39cc fg:#ffffff bold',
               height=Dimension(max=1)),
        text_field]
    )
    layout = Layout(root_container)
    app = Application(layout=layout, full_screen=True,
                      key_bindings=kb, style=style)

    app.run()

    # except Exception as e:
    #     print(e)
    #     target = None
