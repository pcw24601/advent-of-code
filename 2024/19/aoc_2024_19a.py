# Process time: 0.143 seconds.
import time
from functools import cache


def parse_input(lines: list[str]):
    # need frozenset for caching later
    towels = frozenset(map(lambda s: s.strip(), lines[0].split(',')))
    patterns = lines[2:]

    return towels, patterns


@cache
def match_towels(towels: frozenset[str], pattern: str) -> bool:
    if pattern == '':
        return True
    for towel in towels:
        if pattern.startswith(towel):
            if match_towels(towels, pattern.removeprefix(towel)):
                return True
    return False


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    towels, patterns = parse_input(lines)
    answer = sum(map(lambda pattern: match_towels(towels, pattern), patterns))

    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
