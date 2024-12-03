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
    data = []
    with open(inputfile, "r") as f:
        for line in f:
            data.append([int(x) for x in line.strip().split()])

    return data


def __part_1(gamedata):
    answer = 0
    for report in gamedata:
        safe = True
        reason = None
        asc = None
        last = None
        for value in report:
            if last is None:
                last = value
                continue
            diff = value - last

            # Diff by at least 1
            if diff == 0:
                safe = False
                reason = f"No difference ({last},{value})"
                break

            # Diff by at most 3
            if abs(diff) > 3:
                safe = False
                reason = f"Difference greater than 3 ({last} -> {value})"
                break

            last = value
            # See which direction we're going
            if asc is None:
                asc = diff > 0
            else:
                if asc:
                    if diff < 0:
                        safe = False
                        reason = "Direction changed (was asc, now desc)"
                        break
                else:
                    if diff > 0:
                        safe = False
                        reason = "Direction changed (was desc, now asc)"
                        break
        if safe:
            print(f"{report} is safe")
            answer += 1
        else:
            print(f"{report} is unsafe: {reason}")

    print(f"\nPart 1 answer is: {answer}")


def __part_2(gamedata):
    # implement part two here
    raise NotImplementedError("Solution 2 is not yet implemented!")


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
        __part_1(gamedata=gamedata)

    elif index == 2:
        logger.info(">>> Solving for part 2")
        __part_2(gamedata=gamedata)

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)


if __name__ == "__main__":
    main()
