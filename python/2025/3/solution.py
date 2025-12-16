#!/usr/bin/env -S uv run

import time

from rich import print
from rich.traceback import install as rich_install
from rich.console import Console
from rich.table import Table
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)

rich_install(show_locals=True)

DEBUG = False


def debug_print(console: Console, text: str, end: str = "\n"):
    if not DEBUG:
        return
    console.print(text, end=end)


def get_input(path: str):
    with open(path, "r") as f:
        data = f.read().splitlines()

    return data


def split_string_to_int_array(the_string: str) -> list[int]:
    ret = []
    for i in range(0, len(the_string)):
        ret.append(int(the_string[i]))

    return ret


def main(input_path: str, expected1: int = 0, expected2: int = 0):
    console = Console()
    if DEBUG:
        ...

    input_data = get_input(input_path)
    sum_joltage = 0
    sum_joltage2 = 0

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
        transient=True,
    ) as p:
        t1 = p.add_task("Processing...", total=len(input_data))
        for bank in input_data:
            p.update(t1, advance=1)
            p.console.print(bank)
            highest_0 = 0
            highest_1 = 0
            int_array = split_string_to_int_array(bank)
            # find the highest first digit that is not at the end
            found_at = None
            for i in range(0, len(int_array) - 1):
                if int_array[i] > highest_0:
                    highest_0 = int_array[i]
                    found_at = i
            debug_print(console, f"{highest_0=}: {found_at=}")
            # find highest second digit that's after the first
            for i in range(found_at + 1, len(int_array)):
                if int_array[i] > highest_1:
                    highest_1 = int_array[i]
                    found_at = i
            debug_print(console, f"{highest_1=}: {found_at=}")

            value = int(f"{highest_0}{highest_1}")
            sum_joltage += value

    if sum_joltage != expected1:
        raise ValueError(f"{sum_joltage=} should be {expected1}")

    console.print(f"Matches: 1:{sum_joltage} 2:{sum_joltage + sum_joltage2}")


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt", 357)
    print("-------------------- input.txt --------------------")
    main("input.txt", 16946)
