#!/usr/bin/env python
import re
import rich_click as click

from rich import print
from rich.traceback import install
install(show_locals=True)


@click.command(help="Run the solution for a part: 1|2")
@click.argument('index', type=int)
@click.option('--debug', '-d', is_flag=True, default=False, help="Ouput debugging info")
def main(index: int, debug: bool):
    inputfile = 'input.txt'
    total = 0
    if index == 1:
        print(">>> Solving for part 1")
        digit_re = r'([0-9])'
        with open(inputfile, 'r') as f:
            for line in f:
                first, last = None, None
                value = line.strip()
                if debug: print(value)
                items = re.findall(digit_re, value)
                first = items[0]
                last = items[-1]
                if debug: print(first, last)
                number = int(first + last)
                if debug: print(number)
                total += number

    elif index == 2:
        print(">>> Solving for part 2")
        number_re = r'(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))'
        # Lookahead    ^^^
        # This sovles the problem with '4eight5mjlkzrgnmlnmxntqmtlxmqlkjccttcpmgznfouroneightk'
        # where the 'oneight' problem at the end won't get both 'one' and 'eight' otherwise.
        number_values = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9
        }
        with open(inputfile, 'r') as f:
            for line in f:
                first, last = None, None
                value = line.strip()
                if debug: print(f"{value}:")
                items = re.findall(number_re, value)
                if debug: print(items)
                if debug: print(f"  {items[0]}")
                try:
                    first = int(items[0])
                except ValueError:
                    first = number_values[items[0]]
                if debug: print(f"  {items[-1]}")
                try:
                    last = int(items[-1])
                except ValueError:
                    last = number_values[items[-1]]
                if debug: print(first, last)
                number = int(str(first) + str(last))
                if debug: print(f"> {number}")
                total += number

    else:
        print("Invalid index; valid values are 1|2.")
        exit(1)

    print(f"Answer: {total}")


if __name__ == "__main__":
    main()
