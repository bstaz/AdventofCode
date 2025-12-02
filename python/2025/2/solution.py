#!/usr/bin/env -S uv run

from rich import print
from rich.traceback import install as rich_install
from rich.console import Console
from rich.table import Table

rich_install(show_locals=True)

DEBUG = False


def debug_print(text: str, end: str = "\n"):
    if not DEBUG:
        return
    print(text, end=end)


def get_input(path: str):
    data = []
    with open(path, "r") as f:
        data = f.read().splitlines()

    return data


def main(input_path: str, expected1: int = 0, expected2: int = 0):
    console = Console()
    if DEBUG:
        ...

    test_input = get_input(input_path)


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt")
    print("-------------------- input.1.txt --------------------")
    main("input.1.txt")

