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
        return f.readlines()


def __parse_input(data: list[str]):
    rules = {}
    updates = []
    for line in data:
        line = line.strip()
        if "|" in line:
            rule = {"before": []}
            a, b = line.split("|")
            if a in rules.keys():
                rule = rules[a]
            rule["before"].append(b)
            rules[a] = rule
        if "," in line:
            updates.append(line.split(","))

    return (rules, updates)


def __part_1(gamedata) -> int:
    answer = 0

    rules, updates = gamedata
    for update in updates:
        logger.debug(f"Update: {update}")

        for i, page in enumerate(update):
            # Skip the first page and pages with no rules
            if i == 0 or page not in rules.keys():
                continue
            logger.debug(f"Page: {page}, Rules: {rules[page]}")
            for testpage in update[:i]:
                logger.debug(f"Checking {testpage}")
                if testpage in rules[page]["before"]:
                    logger.debug(f"Page {page} fails due to {testpage}!")
                    break
            else:
                continue
            logger.debug("Update fails!")
            break
        else:
            logger.debug("Update succeeds!")
            middle = update[int(len(update) / 2)]
            answer += int(middle)

    return answer


def __part_2(gamedata) -> int:
    # implement part one here
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
