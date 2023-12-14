#!/usr/bin/env python
import os, sys
import logging

import rich_click as click
from rich import print


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()


class SolutionNotImplementedError(NotImplementedError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(args[0])


def parse_input(inputfile: str):
    with open(inputfile, "r") as f:
        raise NotImplementedError("parse_input is not yet implemented!")


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
        # implement part one here
        raise NotImplementedError("Solution 1 is not yet implemented!")

    elif index == 2:
        logger.info(">>> Solving for part 2")
        # implement part two here
        raise NotImplementedError("Solution 2 is not yet implemented!")

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
