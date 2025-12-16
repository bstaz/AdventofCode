#!/usr/bin/env -S uv run

import time

from rich import print
from rich.traceback import install as rich_install
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, MofNCompleteColumn

rich_install(show_locals=True)

DEBUG = True


def debug_print(console: Console, text: str, end: str = "\n"):
    if not DEBUG:
        return
    console.print(text, end=end)


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

    with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
            transient=True,
        ) as p:
        t1 = p.add_task("Groups...", total=len(input_data))
        for group in input_data:
            p.update(t1, advance=1)
            _start, _end = group
            start = int(_start)
            end = int(_end)

            ranges = range(start, end + 1)
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                MofNCompleteColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
                console=console,
                transient=True,
            ) as p2:
                t2 = p2.add_task("IDs...", total=len(ranges))
                p.console.print(group)
                for v in ranges:
                    p2.update(t2, advance=1)
                    #time.sleep(0.0001)
                    _v = str(v)
                    half = int(len(_v) / 2)
                    first, second = (_v[0:half], _v[half:])
                    if first == second:
                        debug_print(console, f"\tMatch1: {_v=} {first=} {second=}")
                        sum_matches += v


    if sum_matches != expected1:
        raise ValueError(f"{sum_matches=} should be {expected1}")

    console.print(f"Matches: 1:{sum_matches} 2:{sum_matches + sum_matches2}")


if __name__ == "__main__":
    print("=====================================================")
    print("------------------- input.test.txt ------------------")
    main("input.test.txt", 1227775554)
    print("-------------------- input.txt --------------------")
    main("input.txt", 31839939622)

