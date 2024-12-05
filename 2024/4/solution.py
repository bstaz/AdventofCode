#!/usr/bin/env python
import os
import sys
import logging
import copy
from enum import Enum


import rich_click as click
from rich import print


logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s in %(funcName)s: %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger()


class Coord(object):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Coord: ({self.x},{self.y})"


class Direction(Enum):
    N = Coord(0, -1)
    NE = Coord(1, -1)
    E = Coord(1, 0)
    SE = Coord(1, 1)
    S = Coord(0, 1)
    SW = Coord(-1, 1)
    W = Coord(-1, 0)
    NW = Coord(-1, -1)


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
    # logger.debug(gamedata)

    origins = __find_all_origins("X", gamedata)
    for origin in origins:
        coords_m = __search_for_letter("M", gamedata, origin)
        if len(coords_m):
            for direction, coord_m in coords_m:
                coords_a = __search_for_letter("A", gamedata, coord_m, direction)
                highlights = [origin, coord_m]
                if len(coords_a):
                    coords_s = __search_for_letter(
                        "S", gamedata, coords_a[0][1], direction
                    )
                    highlights.append(coords_a[0][1])
                    if len(coords_s):
                        # Found full word
                        highlights.append(coords_s[0][1])
                        # __print_highlighted_string(gamedata, highlights)
                        answer += 1

    return answer


def __part_2(gamedata) -> int:
    answer = 0
    origins = __find_all_origins("A", gamedata)

    for origin in origins:
        ...

    return answer


def __find_all_origins(letter: str, data: list[list[str]]) -> list[Coord]:
    coords = []

    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == letter:
                coords.append(Coord(x, y))

    return coords


def __search_for_letter(
    letter: str,
    data: list[list[str]],
    origin: Coord,
    direction: Direction | None = None,
) -> list[tuple[Direction, Coord]]:
    len_x = len(data[0]) - 1
    len_y = len(data) - 1
    coords = []
    if direction is not None:
        target = Coord(origin.x + direction.value.x, origin.y + direction.value.y)
        # Make sure we're in-bounds
        if target.x < 0 or target.y < 0 or target.y > len_y or target.x > len_x:
            pass
        elif data[target.y][target.x] == letter:
            coords.append((direction, target))
    else:
        # No direction specified; search all directions
        for dir in Direction:
            coords += __search_for_letter(letter, data, origin, dir)

    return coords


def __print_highlighted_string(data: list[list[str]], coords: list[Coord]):
    local_data = copy.deepcopy(data)
    lines_to_print = []
    single = False
    if coords[0].y == coords[1].y:
        single = True
    for coord in coords:
        line = local_data[coord.y]
        line[coord.x] = f"[bold yellow]{line[coord.x]}[/bold yellow]"
        if single:
            lines_to_print = [line]
        else:
            lines_to_print.append(line)

    sep = ["=" for _ in range(0, len(lines_to_print[0]))]
    print("".join(sep))
    for line in lines_to_print:
        print("".join(line))


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
