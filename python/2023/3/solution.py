#!/usr/bin/env python
import os, sys
import logging
from typing import List, Dict, Tuple
import re

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


def parse_input(inputfile: str) -> Tuple[List[Dict], Dict[int, Dict], List[List]]:
    """Parse input file and return a data structure:;

    {
        "numbers": [ {"value": 1234, "x": 0, "y": 0, "len": 4 }, ...],
        "symbols": [ {"value": "#", "x": 0, "y": 0 }, ....],
        "data": [ [ ".", "3", ... ] ... ]
    }

    Args:
        inputfile (str): Path to the input file
    """

    digits = [str(x) for x in range(0, 10)]
    foundnumbers = []
    foundsymbols = {}

    with open(inputfile, "r") as f:
        data = []
        y = 0
        pattern = r"([0-9]+)"
        matchcount = 0
        matchednumbers = []
        for line in f:
            matches = re.findall(pattern, line)
            matchcount += len(matches)
            for match in matches:
                matchednumbers.append(int(match))
            data.append([])
            x = 0
            begin = None
            in_word = False
            numberstr = ""
            for char in line:
                data[y].append(char)
                if not in_word and char in digits:
                    # Beginning of a number
                    begin = x
                    in_word = True
                    numberstr = char
                elif in_word and char in digits:
                    # Continuation of a number
                    numberstr += char
                elif in_word and char not in digits:
                    # A number has ended
                    foundnumbers.append(
                        {
                            "value": int(numberstr),
                            "x": begin,
                            "y": y,
                            "len": len(numberstr),
                        }
                    )
                    begin = None
                    in_word = False

                if char != "." and char not in digits:
                    # if char in symbols:
                    if x not in foundsymbols.keys():
                        foundsymbols[x] = {}
                    foundsymbols[x][y] = char

                x += 1
            y += 1

    if matchcount != len(foundnumbers):
        logger.error(
            f"matchcount ({matchcount}) is different from foundnumbers ({len(foundnumbers)})"
        )
        counter = 0
        for match in matchednumbers:
            if match != foundnumbers[counter]["value"]:
                logger.error(f"{match} != {foundnumbers[counter]['value']}")
                exit(1)
            counter += 1

    return (foundnumbers, foundsymbols, data)


def get_box(number: Dict, bounds: Tuple) -> List[Tuple[int, int]]:
    length, start_x, start_y = number["len"], number["x"], number["y"]
    end_x = start_x + length
    bounds_x, bounds_y = bounds
    range_start_x, range_start_y, range_end_x, range_end_y = (0, 0, 0, 0)
    if start_x > 0:
        range_start_x = start_x - 1
    if start_x == 0:
        range_start_x = start_x
    if end_x < bounds_x:
        range_end_x = end_x
    if end_x == bounds_x:
        range_end_x = end_x - 1
    check_x = range(range_start_x, range_end_x + 1)
    if start_y > 0:
        range_start_y = start_y - 1
    if start_y == 0:
        range_start_y = start_y
    if start_y < bounds_y:
        range_end_y = start_y + 1
    if start_y == bounds_y:
        range_end_y = start_y
    check_y = range(range_start_y, range_end_y + 1)
    # logger.debug(f"{start_x}, {end_x}, {check_x}")
    # logger.debug(f"{start_y}, {check_y}")
    box = []
    for x in check_x:
        for y in check_y:
            box.append((x, y))

    # logger.debug(box)

    return box


def check_box_for_symbols(box: List[Tuple[int, int]], symbols: Dict[int, Dict]):
    for x, y in box:
        try:
            symbol = symbols[x][y]
            return True
        except KeyError:
            pass

    return False


def print_box(box, data):
    cursor = None
    lines = {}
    for x, y in box:
        if not y in lines.keys():
            lines[y] = ""
        lines[y] += str(data[y][x])
    for idx, line in lines.items():
        logger.debug(line)


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
    numbers, symbols, data = parse_input(inputfile)
    answer = 0

    if index == 1:
        logger.info(">>> Solving for part 1")
        bounds = (len(data[0]) - 1, len(data) - 1)
        for number in numbers:
            box = get_box(number, bounds)
            logger.debug("")
            logger.debug(f">> Checking {number['value']}")
            if check_box_for_symbols(box, symbols):
                logger.debug(f"Found symbol in box for number: {number['value']}")
                print_box(box, data)
                answer += number["value"]
            else:
                logger.debug(f"Symbol not found in box for number: {number['value']}")
                print_box(box, data)

    elif index == 2:
        logger.info(">>> Solving for part 2")
        # implement part two here
        raise SolutionNotImplementedError("Solution 2 is not yet implemented!")

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
