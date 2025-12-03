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
        lines = f.read().splitlines()

    for group in lines[0].split(","):
        data.append(tuple(group.split("-")))

    return data


def main(input_path: str, expected1: int = 0, expected2: int = 0):
    console = Console()
    if DEBUG:
        ...

    input_data = get_input(input_path)
    sum_matches = 0
    sum_matches2 = 0

    for group in input_data:
        _start, _end = group
        start = int(_start)
        end = int(_end)

        for v in range(start, end + 1):
            _v = str(v)
            half = int(len(_v) / 2)
            first, second = (_v[0:half], _v[half:])
            if first == second:
                debug_print(f"Match! {_v=} {first=} {second=}")
                sum_matches += v


    console.print(f"Matches: 1:{sum_matches} 2:{sum_matches + sum_matches2}")


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt")
    print("-------------------- input.1.txt --------------------")
    main("input.txt")

