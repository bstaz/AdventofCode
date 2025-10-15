#!/usr/bin/env python
import logging

import rich_click as click


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


def __parse_input(data: list[str]) -> tuple[dict[str, list[str]], list[list[str]]]:
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


def __check_update(update: list[str], rules: dict) -> bool:
    for i, page in enumerate(update):
        # Skip the first page and pages with no rules
        if i == 0 or page not in rules.keys():
            continue
        logger.debug(f"Page: {page}, Rules: {rules[page]}")
        for testpage in update[:i]:
            logger.debug(f"Checking {testpage}")
            if testpage in rules[page]["before"]:
                logger.debug(f"Page {page} fails due to {testpage}!")

                return False

    return True


def __part_1(rules, updates) -> int:
    answer = 0

    for update in updates:
        logger.debug(f"Update: {update}")

        if __check_update(update, rules):
            logger.debug("Update succeeds!")
            middle = update[int(len(update) / 2)]
            answer += int(middle)

    return answer


def __part_2(rules, updates: list[list[str]]) -> int:
    answer = 0

    from functools import cmp_to_key

    def sorter(a, b):
        if b in rules[a]["before"]:
            return 1
        else:
            return -1

    sorter_key = cmp_to_key(sorter)

    bad_updates = []
    for update in updates:
        logger.debug(f"Update: {update}")
        if not __check_update(update, rules):
            bad_updates.append(update)

    for update in bad_updates:
        update.sort(key=sorter_key)

        logger.debug(f"Fixed update: {update}")
        middle = update[int(len(update) / 2)]
        answer += int(middle)

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
    rules, updates = __parse_input(rawdata)

    if index == 1:
        logger.info(">>> Solving for part 1")
        answer = __part_1(rules, updates)

    elif index == 2:
        logger.info(">>> Solving for part 2")
        answer = __part_2(rules, updates)

    else:
        logger.error("Invalid index; valid values are 1|2.")
        exit(1)

    logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()
