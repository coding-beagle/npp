from rich.live import Live
from rich.layout import Layout
from rich import print
from rich.table import Table
from rich.panel import Panel
import time


class Editor():
    current_file = ""

    def __init__(self, file_path=""):
        self.current_file = file_path

        self.layout = Layout()
        self.layout.split_column(Layout(name="header"),
                                 Layout(name="file"),
                                 Layout(name="shortcuts"))

        self.layout["header"].minimum_size = 1
        self.layout["file"].minimum_size = 10
        self.layout["shortcuts"].minimum_size = 2

        self.layout["header"].ratio = 1
        self.layout["file"].ratio = 6
        self.layout["shortcuts"].ratio = 1

        if (self.current_file != ""):
            with open(self.current_file, "r") as file:
                self.current_file_content = file.read()

        self.run()

    def draw_file_info(self) -> Table:
        table = Table.grid(expand=True)
        current_file = self.current_file if self.current_file else "Buffer"
        table.add_row(Panel(f"{current_file}"))
        return table

    def draw_file_content(self) -> Table:
        table = Table.grid(expand=True)
        table.add_column("Line", justify="right", no_wrap=True, ratio=1)
        table.add_column("Separator", justify="left", no_wrap=True, ratio=1)
        table.add_column("Content", justify="left", no_wrap=True, ratio=100)

        for index, row in enumerate(self.current_file_content.split("\n")):
            table.add_row(str(index), "|", row)
        return table

    def draw_shortcuts(self) -> Table:
        table = Table.grid(expand=True)
        shortcuts = "Shortcuts go here"
        table.add_row(Panel(f"{shortcuts}"))
        return table

    def edit_files(self):
        self.layout["header"].update(self.draw_file_info())
        self.layout["file"].update(self.draw_file_content())
        self.layout["shortcuts"].update(self.draw_shortcuts())
        breakpoint()

    def run(self):
        self.edit_files()
        while True:
            try:
                with Live(self.layout, screen=True, refresh_per_second=15) as live_console:
                    time.sleep(0.04)
                    live_console.update(self.edit_files())
            except KeyboardInterrupt:
                print("[bold]Exiting nano++ editor[/bold]")
                break
