#!/usr/bin/env python
import os
import sys
import logging

import rich_click as click
from rich import print


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()


class SolutionNotImplementedError(NotImplementedError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(args[0])


def parse_input(inputfile: str):
    lefts = []
    rights = []
    with open(inputfile, "r") as f:
        contents = f.readlines()
        for line in contents:
            line = line.rstrip()
            left, right = line.split()
            lefts.append(int(left))
            rights.append(int(right))

    if len(rights) != len(lefts):
        raise ValueError("The length of the arrays is not equal!")

    return {"lefts": lefts, "rights": rights}


@click.command(help="Run the solution for a part: 1|2")
@click.argument("index", type=int)
@click.option("--debug", "-d", is_flag=True, default=False, help="Ouput debugging info")
def main(index: int, debug: bool):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging enabled")
        logger.debug("Setting up Rich traceback handler...")
        from rich.traceback import install

        install(show_locals=True)
        logger.debug(" ...Done.")

    inputfile = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/input.txt"
    gamedata = parse_input(inputfile)
    answer = 0

    if index == 1:
        logger.info(">>> Solving for part 1")
        gamedata["lefts"].sort()
        gamedata["rights"].sort()

        for i, x in enumerate(gamedata["lefts"]):
            answer += abs(gamedata["rights"][i] - gamedata["lefts"][i])

        print(f"The answer to Day 1 Part 1 is: {answer}")

    elif index == 2:
        logger.info(">>> Solving for part 2")
        # Get a count of each unique item in the right list
        gamedata["rights"].sort()
        counts = {}
        for value in gamedata["rights"]:
            if value in counts.keys():
                counts[value] += 1
            else:
                counts[value] = 1

        for value in gamedata["lefts"]:
            if value in counts.keys():
                answer += value * counts[value]

        print(f"The answer to Day 1 Part 2 is: {answer}")

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
