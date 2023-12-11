#!/usr/bin/env python
import os, sys

import rich_click as click
from rich import print


def parse_input(inputfile: str):
    with open(inputfile, "r") as f:
        games = {}
        for line in f:
            game, data = line.strip().split(": ")
            gameId = game.split()[1]
            draws = data.split("; ")
            games[gameId] = {}
            drawcounter = 1
            for draw in draws:
                tempdict = {}
                for item in draw.split(", "):
                    count, color = item.split()
                    tempdict[color] = count
                games[gameId][drawcounter] = tempdict
                drawcounter += 1

    return games


@click.command(help="Run the solution for a part: 1|2")
@click.argument("index", type=int)
@click.option("--debug", "-d", is_flag=True, default=False, help="Ouput debugging info")
def main(index: int, debug: bool):
    if debug:
        print("Debugging enabled; setting up Rich traceback handler...")
        from rich.traceback import install
        install(show_locals=True)

    inputfile = f"{os.path.dirname(os.path.abspath(sys.argv[0]))}/input.txt"
    gamedata = parse_input(inputfile)
    answer = 0

    if index == 1:
        print(">>> Solving for part 1")
        maxcubes = {"red": 12, "green": 13, "blue": 14}
        for gameid, draws in gamedata.items():
            if debug:
                print(gameid, draws)
            gamePossible = True
            for drawid, drawdata in draws.items():
                for color, count in drawdata.items():
                    if debug:
                        print(color, count)
                    if int(count) > maxcubes[color]:
                        gamePossible = False

            if gamePossible:
                answer += int(gameid)
            else:
                if debug:
                    print(f">>> {gameid} not possible!")
                    print(f">>> {draws}")

    elif index == 2:
        print(">>> Solving for part 2")
        with open(inputfile, "r") as f:
            for line in [x.strip() for x in f]:
                print(line)

    else:
        print("Invalid index; valid values are 1|2.")
        exit(1)

    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
