#!/usr/bin/env python
import os
import sys
import logging
import re

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
    with open(inputfile, "r") as f:
        data = ""
        for line in f:
            data += line.strip()

    return data


def __part_1(gamedata) -> int:
    answer = 0

    example_data = (
        "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
    pattern = r"(mul\(([0-9]+),([0-9]+)\))"
    # Get all instances of "mul(x,y)"
    matches = re.findall(pattern, gamedata)
    for match in matches:
        logger.debug(match)
        answer += int(match[1]) * int(match[2])

    return answer


def __part_2(gamedata) -> int:
    answer = 0

    example_data = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    pattern = r"(do\(\))|(don't\(\))|(mul\(([0-9]+),([0-9]+)\))"
    # Get all instances of "mul(x,y)"
    matches = re.findall(pattern, gamedata)

    enabled = True
    for match in matches:
        logger.debug(match)
        if enabled and match[2]:
            logger.debug(f"+[bold green]{match[2]}[/bold green]")
            answer += int(match[3]) * int(match[4])
        elif match[1]:
            logger.debug(f"off: {match[1]}")
            enabled = False
        elif match[0]:
            logger.debug(f"on: {match[0]}")
            enabled = True
        else:
            logger.debug(f"-[bold red]{match[2]}[/bold red]")

    return answer


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

    if index == 1:
        logger.info(">>> Solving for part 1")
        answer = __part_1(gamedata=gamedata)

    elif index == 2:
        logger.info(">>> Solving for part 2")
        answer = __part_2(gamedata=gamedata)

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
