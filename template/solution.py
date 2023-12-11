#!/usr/bin/env python
import os, sys

import rich_click as click
from rich import print


def parse_input(inputfile: str):
    with open(inputfile, "r") as f:
        raise NotImplementedError("parse_input is not yet implemented!")


@click.command(help="Run the solution for a part: 1|2")
@click.argument("index", type=int)
@click.option("--debug", "-d", is_flag=True, default=False, help="Ouput debugging info")
def main(index: int, debug: bool):
    if debug:
        print("Debugging enabled; setting up Rich traceback handler...")
        from rich.traceback import install
        install(show_locals=True)

    inputfile = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/input.txt"
    gamedata = parse_input(inputfile)
    answer = 0

    if index == 1:
        print(">>> Solving for part 1")
        # implement part one here
        raise NotImplementedError("Solution 1 is not yet implemented!")

    elif index == 2:
        print(">>> Solving for part 2")
        # implement part two here
        raise NotImplementedError("Solution 2 is not yet implemented!")

    else:
        print("Invalid index; valid values are 1|2.")
        exit(1)

    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
