from rich.live import Live
from rich.layout import Layout
from rich import print
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
import time
from rich import box

from .input_handler import InputHandler


class Editor():
    current_file = ""

    def __init__(self, file_path=""):
        self.console = Console()
        self.current_file = file_path

        self.layout = Layout()
        self.layout.split_column(Layout(name="header"),
                                 Layout(name="file"),
                                 Layout(name="shortcuts"))

        self.layout["header"].minimum_size = 1
        self.layout["file"].minimum_size = 10
        self.layout["shortcuts"].minimum_size = 3

        self.layout["header"].ratio = 1
        self.layout["file"].ratio = 6
        self.layout["shortcuts"].ratio = 1

        if (self.current_file != ""):
            with open(self.current_file, "r") as file:
                self.current_file_content = file.read()

        self.input_handler = InputHandler()

        self.run()

    def draw_file_info(self) -> Table:
        table = Table.grid(expand=True)
        current_file = self.current_file if self.current_file else "Buffer"
        table.add_row(
            Panel(f"Currently editing: [blue][bold]{current_file}[/blue][/bold]"))
        return table

    def draw_file_content(self) -> Table:
        table = Table.grid(expand=True)
        table.add_column("Line", justify="right", no_wrap=True, ratio=1)
        table.add_column("Separator", justify="left", no_wrap=True, ratio=1)
        table.add_column("Content", justify="left", no_wrap=True, ratio=100)

        split_content = self.current_file_content.split("\n")

        for index, row in enumerate(range(self.console.size.height - 3)):
            row_text = split_content[index] if index < len(
                split_content) else ""
            table.add_row(str(index), "|", row_text)

        table.add_row("", "|", f"{self.console.size.height} lines")
        return table

    def draw_shortcuts(self) -> Table:
        table = Table(box=box.SIMPLE)
        shortcuts = "Shortcuts go here"
        current_keys = ""
        for i in self.input_handler.get_currently_pressed_keys():
            current_keys += f"{i} "
        table.add_row(f"Current keys: {current_keys}")
        table.add_row(f"{shortcuts}")
        table.add_row(f"Press [bold]Ctrl + C[/bold] to exit")
        return table

    def edit_files(self):
        self.layout["header"].update(self.draw_file_info())
        self.layout["file"].update(self.draw_file_content())
        self.layout["shortcuts"].update(self.draw_shortcuts())

    def run(self):
        self.edit_files()
        while True:
            try:
                with Live(self.layout, console=self.console, screen=True, refresh_per_second=1, transient=True) as live_console:
                    time.sleep(0.04)
                    live_console.update(self.edit_files())
                    # breakpoint()
            except KeyboardInterrupt:
                print("[bold]Exiting nano++ editor[/bold]")
                break
