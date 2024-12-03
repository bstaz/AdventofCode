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
        print(f"{report} ", end="")

        if __check_report(report):
            print("\t[bold green]SAFE[/bold green]")
            answer += 1

    print(f"\nPart 1 answer is: {answer}")


def __print_unsafe(message: str):
    print(f"\t[bold red]UNSAFE[/bold red]: {message}")


def __part_2(gamedata: list[list[int]]):
    answer = 0
    for report in gamedata:
        print(f"{report} ", end="")

        if __check_report(report):
            print("\t[bold green]SAFE[/bold green]")
            answer += 1
        else:
            length = len(report)
            retry_count = 0
            while retry_count < length:
                retry = report.copy()
                popped = retry.pop(retry_count)
                retry_count += 1
                print(f"\t{retry} (p:{popped}) ", end="")
                if __check_report(retry):
                    print("\t[bold green]SAFE[/bold green]")
                    answer += 1
                    break

    print(f"\nPart 2 answer is: {answer}")


def __check_report(report):
    asc = None
    last = None
    for value in report:
        if last is None:
            last = value
            continue
        diff = value - last

        # Diff by at least 1
        if diff == 0:
            reason = f"No difference ({last},{value})"
            __print_unsafe(reason)
            return False

        # Diff by at most 3
        if abs(diff) > 3:
            reason = f"Difference greater than 3 ({last} -> {value})"
            __print_unsafe(reason)
            return False

        # See which direction we're going
        if asc is None:
            asc = diff > 0
        else:
            if asc:
                if diff < 0:
                    reason = "Direction changed (was asc, now desc)"
                    __print_unsafe(reason)
                    return False
            else:
                if diff > 0:
                    reason = "Direction changed (was desc, now asc)"
                    __print_unsafe(reason)
                    return False
        last = value

    return True


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
