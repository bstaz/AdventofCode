#!/usr/bin/env python
import os
import sys
import logging
import copy

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


def __load_input_from_file(inputfile: str):
    with open(inputfile, "r") as f:
        return f.readlines()


def __parse_input(data):
    ret = []
    for line in data:
        line = list(line.strip())
        ret.append(line)

    return ret


def __part_1(gamedata) -> int:
    answer = 0
    logger.debug(gamedata)

    for y, line in enumerate(gamedata):
        logger.debug(f"line: {"".join(line)}")
        for x, letter in enumerate(line):
            if letter == "X":
                logger.debug(f"X found at {x},{y}")
                coords = [(x, y)]
                # __print_highlighted_string(gamedata, [(x, y)])
                coords_m = __search_for_letter("M", gamedata, [x, y])
                if len(coords_m):
                    for coord_m in coords_m:
                        coords_a = __search_for_letter("A", gamedata, list(coord_m))
                        if len(coords_a):
                            for coord_a in coords_a:
                                coords_s = __search_for_letter(
                                    "S", gamedata, list(coord_a)
                                )
                                if len(coords_s):
                                    coords.append(coord_m)
                                    coords.append(coord_a)
                                    coords += coords_s
                    __print_highlighted_string(gamedata, set(coords))

    return answer


def __search_for_letter(
    letter: str, data: list[list[str]], origin: list[int]
) -> list[tuple[int, int]]:
    len_x = len(data[0]) - 1
    len_y = len(data) - 1
    coords = []
    for xx in range(-1, 2):
        # Stay in-bounds
        search_x = origin[0] + xx
        if search_x < 0 or search_x > len_x:
            continue
        for yy in range(-1, 2):
            # Stay in-bounds
            search_y = origin[1] + yy
            # Skip the origin
            if xx == 00 and yy == 00:
                continue
            if search_y < 0 or search_y > len_y:
                continue
            logger.debug(f"Searching {search_x},{search_y}")
            if data[search_x][search_y] == letter:
                logger.debug(f"Found '{letter}' at {search_x},{search_y}")
                coords.append((search_x, search_y))

    return coords


def __print_highlighted_string(data: list[list[str]], coords: set[tuple[int, int]]):
    local_data = copy.deepcopy(data)
    lines_to_print = set()
    for coord in coords:
        line = local_data[coord[0]]
        line[coord[1]] = f"[bold yellow]{line[coord[1]]}[/bold yellow]"
        lines_to_print.add(coord[0])

    for line in lines_to_print:
        print("".join(local_data[line]))


def __part_2(gamedata) -> int:
    # implement part one here
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

    inputfile = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/example.txt"
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
