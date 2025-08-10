from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="nanoplusplus",
    version="0.3.4",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["Click", "Prompt_Toolkit", "Pyperclip"],
    entry_points={
        "console_scripts": [
            "npp = nanoplusplus.main:cli",
        ],
    },
)
