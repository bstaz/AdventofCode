#!/usr/bin/env -S uv run

from rich import print
from rich.traceback import install as rich_install
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)

rich_install(show_locals=True)

DEBUG = True


def debug_print(console: Console, text: str, end: str = "\n"):
    if not DEBUG:
        return
    console.print(text, end=end)


def get_input(path: str):
    with open(path, "r") as f:
        data = f.read().splitlines()

    grid = [list(line) for line in data]

    return grid


def get_surrounding_rolls(x: int, y: int, grid) -> int:
    return 0


def main(input_path: str, expected1: int = 0, expected2: int = 0):
    console = Console()
    if DEBUG:
        ...

    grid = get_input(input_path)
    rolls1 = 0
    rolls2 = 0


    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    ) as p:
        t1 = p.add_task("Processing...", total=len(grid))

        console.print(grid)

        print("")
        for row in range(0, len(grid)):
            for col in range(0, len(grid[row])):
                if grid[row][col] == "@" and get_surrounding_rolls(col, row, grid) < 4:
                    rolls1 += 1
            print("")

    if expected1 and rolls1 != expected1:
        raise ValueError(f"{rolls1=} should be {expected1}")
    if expected2 and rolls2 != expected2:
        raise ValueError(f"{rolls2=} should be {expected2}")

    console.print(f"Rolls: 1: {rolls1} 2: {rolls2}")


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt")
    #print("-------------------- input.txt --------------------")
    #main("input.txt")

