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

    answer = None

    if index == 1:
        print(">>> Solving for part 1")
        #implement part one here
        pass

    elif index == 2:
        print(">>> Solving for part 2")
        #implement part two here
        pass

    else:
        print("Invalid index; valid values are 1|2.")
        exit(1)

    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()