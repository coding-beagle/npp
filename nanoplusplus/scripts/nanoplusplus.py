import click
from pathlib import Path


@click.command()
# @click.option("path")
def cli(path: str = "hello") -> int:
    """Open a file in the NanoPlusPlus text editor!"""
    target_dir = Path(path)
    if not target_dir.exists():
        click.echo("The target directory doesn't exist")
        raise SystemExit(1)
    else:
        print(f"Opening {path} in Nano Plus Plus!")


def editor()
