#!/usr/bin/env python
import logging

import rich_click as click
from rich import print


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s in %(funcName)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()


class SolutionNotImplementedError(NotImplementedError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        logger.error(args[0])


def __load_input_from_file(inputfile: click.Path):
    with open(str(inputfile), "r") as f:
        raise NotImplementedError("load_input_from_file is not yet implemented!")


def __parse_input(data):
    raise NotImplementedError("parse_input is not yet implemented!")


def __part_1(gamedata) -> int:
    # implement part one here
    raise NotImplementedError("Solution 1 is not yet implemented!")


def __part_2(gamedata) -> int:
    # implement part two here
    raise NotImplementedError("Solution 2 is not yet implemented!")


@click.command(help="Run the solution for a part: 1|2")
@click.argument("index", type=int)
@click.argument(
    "inputfile", type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.option("--debug", "-d", is_flag=True, default=False, help="Ouput debugging info")
def main(index: int, debug: bool, inputfile: click.Path):
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debugging enabled")
        logger.debug("Setting up Rich traceback handler...")
        from rich.traceback import install

        install(show_locals=True)
        logger.debug(" ...Done.")

    rawdata = __load_input_from_file(inputfile)
    gamedata = __parse_input(rawdata)

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
