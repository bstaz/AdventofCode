#!/usr/bin/env python
import rich_click as click
from rich import print


@click.command(help="Run the solution for a part: 1|2")
@click.argument('index', type=int)
@click.option('--debug', '-d', is_flag=True, default=False, help="Ouput debugging info")
def main(index: int, debug: bool):
    if debug:
        print("Debugging enabled; setting up Rich traceback handler...")
        from rich.traceback import install
        install(show_locals=True)

    inputfile = 'input.txt'
    answer = 0

    if index == 1:
        print(">>> Solving for part 1")
        maxcubes = {
            'red': 12,
            'green': 13,
            'blue': 14
        }
        with open(inputfile, 'r') as f:
            for line in f:
                game, data = line.strip().split(': ')
                gameId = game.split()[1]
                draws = data.split('; ')
                if debug: print(gameId, draws)
                gamePossible = True
                for draw in draws:
                    for item in draw.split(', '):
                        if debug: print(item)
                        count, color = item.split()
                        if int(count) > maxcubes[color]:
                            gamePossible = False

                if gamePossible:
                    answer += int(gameId)
                else:
                    if debug: print(f">>> {gameId} not possible!")
                    if debug: print(f">>> {line.strip()}")

    elif index == 2:
        print(">>> Solving for part 2")
        with open(inputfile, 'r') as f:
            for line in [x.strip() for x in f]:
                print(line)

    else:
        print("Invalid index; valid values are 1|2.")
        exit(1)

    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
