# Process time: 0.00104 seconds.
import re
import time
from collections import defaultdict
import itertools


def create_map(grid: list[str]) -> defaultdict[str,set[tuple[int,int]]]:
    antennae_positions: defaultdict[str,set[tuple[int,int]]] = defaultdict(set)
    for row_num, row in enumerate(grid):
        matches = re.finditer("[A-Za-z0-9]", row)
        for match in matches:
            antennae_positions[match.group(0)].add((row_num, match.start()))
    return antennae_positions
    # E.g. {'0': {(4, 4), (3, 7), (1, 8), (2, 5)}, 'A': {(8, 8), (5, 6), (9, 9)}}


def create_antinodes_one_freq(
        antennae_positions: set[tuple[int, int]],
        num_rows: int, num_cols: int
) -> set[tuple[int, int]]:
    antinodes = set()
    for (a1_row, a1_col), (a2_row, a2_col) in itertools.combinations(antennae_positions, r=2):
        multiplier = 0
        finished = False
        while not finished:
            finished = True
            row_diff = (a1_row - a2_row) * multiplier
            col_diff = (a1_col - a2_col) * multiplier
            anode1_row = a1_row + row_diff
            anode1_col = a1_col + col_diff
            anode2_row = a2_row - row_diff
            anode2_col = a2_col - col_diff
            if (0 <= anode1_row < num_rows) and (0 <= anode1_col < num_cols):
                antinodes.add((anode1_row, anode1_col))
                finished = False
            if (0 <= anode2_row < num_rows) and (0 <= anode2_col < num_cols):
                antinodes.add((anode2_row, anode2_col))
                finished = False
            multiplier += 1

    return antinodes


def main():
    fname = 'input.txt'
    # fname='test.txt'

    with open(fname, 'r') as fp:
        grid = fp.read().splitlines()

    num_rows = len(grid)
    num_cols = len(grid[0])

    antennae_positions = create_map(grid)
    antinodes = set()
    for antennae_positions_one_freq in antennae_positions.values():
        antinodes |= create_antinodes_one_freq(antennae_positions_one_freq, num_rows, num_cols)

    print(f'{len(antinodes)=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
