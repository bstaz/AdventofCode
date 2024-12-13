#!/usr/bin/env python
import logging
from enum import Enum
import copy
import time

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


class Coord(object):
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Coord):
            raise TypeError(f"Cannot add {type(other)} to Coord")
        else:
            return Coord(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"{self.x},{self.y}"


class Direction(Enum):
    North = Coord(0, -1)
    East = Coord(1, 0)
    South = Coord(0, 1)
    West = Coord(-1, 0)


def __load_input_from_file(inputfile: click.Path):
    with open(str(inputfile), "r") as f:
        return f.readlines()


def __parse_input(data) -> tuple[list[list[str]], Coord]:
    ret = []
    for y, line in enumerate(data):
        chars = []
        for x, char in enumerate(line.strip()):
            chars.append(char)
            if char == "^":
                start = Coord(x, y)
        ret.append(chars)

    return (ret, start)


def __part_1(map: list[list[str]], start: Coord) -> int:
    current: Coord = start
    direction: Direction = Direction.North
    answer = 0
    visited = set()
    visited.add(str(current))
    # visited_map = map.copy()
    # visited_map[current.y][current.x] = "S"
    out_of_bounds = False

    while not out_of_bounds:
        move = current + direction.value
        try:
            if move.x < 0 or move.y < 0:
                raise IndexError
            contents = map[move.y][move.x]
            if contents != "#":
                current = move
                # match direction:
                #     case Direction.North:
                #         visited_map[current.y][current.x] = "^"
                #     case Direction.East:
                #         visited_map[current.y][current.x] = ">"
                #     case Direction.South:
                #         visited_map[current.y][current.x] = "v"
                #     case Direction.West:
                #         visited_map[current.y][current.x] = "<"
                visited.add(str(current))
                answer = len(visited)
            else:
                match direction:
                    case Direction.North:
                        direction = Direction.East
                    case Direction.East:
                        direction = Direction.South
                    case Direction.South:
                        direction = Direction.West
                    case Direction.West:
                        direction = Direction.North
        except IndexError:
            out_of_bounds = True

    answer = len(visited)

    # for line in visited_map:
    #     for char in line:
    #         print(char, end="")
    #     print("")

    return answer


def __check_for_loop(map: list[list[str]], start: Coord, obstruction: Coord) -> bool:
    current: Coord = start
    direction: Direction = Direction.North
    visited = set()
    visited.add(str(current))
    test_map = copy.deepcopy(map)
    test_map[obstruction.y][obstruction.x] = "#"
    visited_map = copy.deepcopy(map)
    visited_map[current.y][current.x] = "S"
    out_of_bounds = False
    turns_without_new_spaces = 0
    new_space_counter = 0
    new_spaces_since_last_turn = 0

    # print(f"Testing {obstruction}")
    if obstruction.x == 3 and obstruction.y == 6:
        pass

    while not out_of_bounds:
        move = current + direction.value
        try:
            if move.x < 0 or move.y < 0:
                raise IndexError
            contents = test_map[move.y][move.x]
            if contents != "#":
                current = move
                match direction:
                    case Direction.North:
                        visited_map[current.y][current.x] = "^"
                    case Direction.East:
                        visited_map[current.y][current.x] = ">"
                    case Direction.South:
                        visited_map[current.y][current.x] = "v"
                    case Direction.West:
                        visited_map[current.y][current.x] = "<"
                before = len(visited)
                visited.add(str(current))
                after = len(visited)
                new_space_counter += after - before
            else:
                new_spaces_since_last_turn = new_space_counter
                new_space_counter = 0
                if new_spaces_since_last_turn == 0:
                    turns_without_new_spaces += 1
                if turns_without_new_spaces > 4:
                    return True
                match direction:
                    case Direction.North:
                        direction = Direction.East
                    case Direction.East:
                        direction = Direction.South
                    case Direction.South:
                        direction = Direction.West
                    case Direction.West:
                        direction = Direction.North
        except IndexError:
            out_of_bounds = True

    # for line in visited_map:
    #     for char in line:
    #         print(char, end="")
    #     print("")

    return False


def __part_2(map: list[list[str]], start: Coord) -> int:
    answer = 0

    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char != "#" and Coord(x, y) != start:
                if __check_for_loop(map=map, start=start, obstruction=Coord(x, y)):
                    print(f"Found loop at {x},{y}")
                    answer += 1

    return answer


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
    map, start = __parse_input(rawdata)

    begin = time.time_ns()
    if index == 1:
        logger.info(">>> Solving for part 1")
        answer = __part_1(map, start)

    elif index == 2:
        logger.info(">>> Solving for part 2")
        answer = __part_2(map, start)

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)
    elapsed = time.time_ns() - begin
    print(elapsed / 1_000_000)

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
