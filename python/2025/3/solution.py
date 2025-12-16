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


def get_highest(haystack: list[int], start: int, pad: int) -> tuple[int, int]:
    highest = 0
    found_at = 0
    to_check = range(start, len(haystack) - pad)
    for i in to_check:
        if haystack[i] > highest:
            highest = haystack[i]
            found_at = i
            if highest == 9:
                break

    return (highest, found_at)


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
            highest_0 = 0
            highest_1 = 0
            int_array = split_string_to_int_array(bank)

            # Part 1
            found_at = None
            # find the highest first digit that is not at the end
            highest_0, found_at = get_highest(int_array, 0, 1)
            debug_print(console, f"{highest_0=}: {found_at=}")

            # find highest second digit that's after the first
            highest_1, found_at = get_highest(int_array, found_at + 1, 0)
            debug_print(console, f"{highest_1=}: {found_at=}")

            value = int(f"{highest_0}{highest_1}")
            sum_joltage += value

            # Part 2
            found_at = 0
            pad = 12
            value_arr = []
            for i in range(0, pad):
                pad -= 1
                highest, found_at = get_highest(int_array, found_at, pad)
                debug_print(console, f"{highest=} {found_at=}")
                found_at += 1
                value_arr.append(highest)
            value = "".join(str(x) for x in value_arr)
            debug_print(console, f"{value=}")
            sum_joltage2 += int(value)

    if expected1 and sum_joltage != expected1:
        raise ValueError(f"{sum_joltage=} should be {expected1}")
    if expected2 and sum_joltage2 != expected2:
        raise ValueError(f"{sum_joltage2=} should be {expected2}")

    console.print(f"Joltages: 1: {sum_joltage} 2: {sum_joltage2}")


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt", 357, 3121910778619)
    print("-------------------- input.txt --------------------")
    main("input.txt", 16946, 168627047606506)
