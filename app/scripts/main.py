import click
from editor import Editor
from rich import print


@click.group()
def cli():
    pass

# entry point should be kept pretty simple


@cli.command()
@click.argument('file_path', required=False)
def npp(file_path: str = ""):
    """ FILE_PATH: Path to the file to be opened in nano++ """
    print(f"Opening nano++ editor, with file: {file_path}")
    editor = Editor(file_path)


if __name__ == '__main__':
    exit(cli())
