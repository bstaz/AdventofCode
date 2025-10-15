#!/usr/bin/env python
import logging
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


def __load_input_from_file(inputfile: click.Path):
    ret = []
    with open(str(inputfile), "r") as f:
        for line in f:
            ret.append(line.strip())

    return ret


def __parse_input(data) -> list[tuple[int, list[int]]]:
    ret = []
    for line in data:
        value, operands = line.split(":")
        ret.append((int(value), [int(x) for x in operands.split()]))

    return ret


def __do_math(value: int, a: int, b: list[int]) -> bool:
    if len(b) > 1:
        if __do_math(value, a + b[0], b[1:]) or __do_math(value, a * b[0], b[1:]):
            return True
        else:
            return False
    elif a + b[0] == value or a * b[0] == value:
        return True
    else:
        return False


def __get_concat_permutations(input: list[int]) -> list[list[int]]:
    ret = []
    """
    10 19 -> [1019]
    81 40 27 -> [8140 27], [81 4027]
    """

    if len(input) == 2:
        return [[int(str(input[0]) + str(input[1]))]]
    else:
        ret.append()

    return ret


def __do_math_with_concat(value: int, operands: list[int]) -> bool:
    if len(operands) == 2 and value == int(str(operands[0]) + str(operands[1])):
        return True
    # Generate permutations of operands[] with each possible set concatenated
    remaining = len(operands) - 1
    while remaining > 1:
        ...

    return False


def __part_1(gamedata) -> int:
    answer = 0

    for value, operands in gamedata:
        if __do_math(value, operands[0], operands[1:]):
            answer += value

    return answer


def __part_2(gamedata) -> int:
    answer = 0

    for value, operands in gamedata:
        if __do_math(value, operands[0], operands[1:]) or __do_math_with_concat(
            value, operands
        ):
            answer += value

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
    gamedata = __parse_input(rawdata)

    begin = time.time_ns()
    if index == 1:
        logger.info(">>> Solving for part 1")
        answer = __part_1(gamedata=gamedata)

    elif index == 2:
        logger.info(">>> Solving for part 2")
        answer = __part_2(gamedata=gamedata)

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)
    print(f"Elapsed: {(time.time_ns() - begin) / 1_000_000}")

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
