#!/usr/bin/env -S uv run

from rich import print
from rich.traceback import install as rich_install
rich_install(show_locals=True)

DEBUG=True

def debug_print(text: str, end: str = "\n"):
    if not DEBUG:
        return
    print(text, end=end)

def get_input(path: str):
    data = []
    with open(path, "r") as f:
        data = f.read().splitlines()

    return data


def main(input_path: str):
    print("=========================================")
    test_input = get_input(input_path)
    start = 50
    current = start
    zero_count = 0
    line_count = 0
    for line in test_input:
        line_count += 1
        direction = line[0]
        distance = int(line[1:])
        debug_print(f"S:{current} {direction}:{distance} B:", end="")
        if direction == "L":
            current -= distance
            debug_print(f"{current}", end="")
            if current < 0:
                adjustment = (abs(int(current / 100)) + 1) * 100
                debug_print(f" adj:{adjustment}", end="")
                current += adjustment
        else:
            current += distance
            debug_print(f"{current}", end="")
            if current >= 100:
                adjustment = int(current / 100) * 100
                debug_print(f" adj:{adjustment}", end="")
                current -= adjustment

        if current % 100 == 0:
            current = 0

        debug_print(f" A:{current}", end="")
        if current < -100000 or current > 100000:
            print("\n[bold red]Something has gone wrong![/bold red]")
            exit(1)
        if current == 0:
            debug_print("[bold green] +1[/bold green]")
            zero_count += 1
        else:
            debug_print("")

    print(f"Solution for {input_path} is {zero_count}")


if __name__ == "__main__":
    main("input.test.txt")
    main("input.1.txt")

