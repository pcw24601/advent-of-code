# Process time: 0.0565 seconds.
import time
from itertools import product
from typing import Literal


def parse_input(in_string: str) -> tuple[list, list]:
    entries = in_string.split('\n\n')
    components = {'keys': [], 'locks': []}
    for entry in entries:
        type, heights = create_lock_or_key(entry)
        components[type].append(heights)
    return components['locks'], components['keys']


def create_lock_or_key(entry: str) -> tuple[Literal['key', 'lock'], list[int]]:
    entry_list = entry.split()
    if entry_list[0] == '#' * 5:
        type = 'keys'
    else:
        type = 'locks'
    height = [0] * 5
    for row in entry_list[1:6]:  # Omit top and bottom rows, they will be all '#' or '.'
        for col, symbol in enumerate(row):
            if symbol == '#':
                height[col] += 1
    return type, height


def check_fit(lock, key):
    # Return True if key fits in lock
    fails = sum(map(lambda x: x[0] + x[1] > 5, zip(lock, key)))
    return fails == 0



def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        in_string = fp.read()

    locks, keys = parse_input(in_string)
    answer = sum(map(check_fit, *zip(*product(locks, keys))))
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
