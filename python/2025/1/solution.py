#!/usr/bin/env -S uv run

import math

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
        table = Table(title="Debug")
        table.add_column("Start")
        table.add_column("Direction")
        table.add_column("Before Adj")
        table.add_column("Adj")
        table.add_column("After adj")
        table.add_column("Counts")

    test_input = get_input(input_path)
    current = 50
    zero_count = 0
    zero_count_2 = 0
    line_count = 0
    for line in test_input:
        line_count += 1
        direction = line[0]
        distance = int(line[1:])
        _dir_dist = f"{direction}:{distance}"
        adjustment = 0
        revolutions = math.floor(distance / 100)
        remainder = distance - (revolutions * 100)
        zero_count_2_add = revolutions
        _start = str(current)
        start = current

        if direction == "L":
            current -= remainder
            _before_adj = str(current)
            if current < 0:
                if start != 0:
                    zero_count_2_add += 1
                adjustment = 100
        else:
            current += remainder
            _before_adj = str(current)
            if current > 100:
                zero_count_2_add += 1
                adjustment = -100

        current += adjustment

        if current == 100:
            current = 0
        _after_adj = str(current)

        if current < 0 or current > 99:
            raise ValueError(f"current is out of bounds: {current=}")

        _counts = f" ([bold red]+{zero_count_2_add}[/bold red]"
        if zero_count_2_add != 0:
            zero_count_2 += zero_count_2_add

        if current < -10000 or current > 10000:
            console.print("\n[bold red]Something has gone wrong![/bold red]")
            console.print(f"Current is {current}; zero_count is {zero_count}")
            exit(1)

        if current == 0:
            _counts += " [bold green]+1[/bold green])"
            zero_count += 1
        else:
            _counts += ")"

        if DEBUG:
            table.add_row(
                _start,
                _dir_dist,
                _before_adj,
                str(adjustment),
                _after_adj,
                _counts,
            )

    console.print(table) if DEBUG else None

    if expected1 and expected1 != zero_count:
        console.print(
            f"[bold red]Solution 1 for {input_path}: {zero_count} does not match {expected1}"
        )
    else:
        console.print(f"Solution 1 for {input_path} is {zero_count}")
    if expected2 and expected2 != zero_count + zero_count_2:
        console.print(
            f"[bold red]Solution 2 for {input_path}: {zero_count_2} does not match {expected2}"
        )
    else:
        console.print(f"Solution 2 for {input_path} is {zero_count + zero_count_2}")


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt", expected1=3, expected2=6)
    print("------------------ input.test2.txt ------------------")
    main("input.test2.txt", expected1=4, expected2=15)
    print("-------------------- input.1.txt --------------------")
    main("input.1.txt", expected1=1182, expected2=6907)
