# Process time: 0.0165 seconds.
import time
from itertools import product

def find_perim_area(row, col, grid, unprocessed_points, num_rows, num_cols) -> tuple[int, int]:
    area = 1
    perim = 0
    for row_diff, col_diff in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        current_plant = grid[row][col]
        new_row = row + row_diff
        new_col = col + col_diff
        if (0 <= new_row < num_rows) and (0 <= new_col < num_cols):
            # Not edge
            new_plant = grid[new_row][new_col]
            if new_plant == current_plant:
                # Same plot
                if (new_row, new_col) in unprocessed_points:
                    unprocessed_points.remove((new_row, new_col))
                    this_area, this_perim = find_perim_area(new_row, new_col, grid, unprocessed_points, num_rows, num_cols)
                    area += this_area
                    perim += this_perim
            else:
                # border with different plot
                perim += 1
        else:
            # Edge piece
            perim += 1

    return area, perim


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        grid = fp.read().splitlines()

    num_rows = len(grid)
    num_cols = len(grid[0])
    unprocessed_points = set(product(range(num_rows), range(num_cols)))
    cost = 0
    while unprocessed_points:
        row, col = unprocessed_points.pop()
        area, perim = find_perim_area(row, col, grid, unprocessed_points, num_rows, num_cols)
        cost += area * perim
    print(f'{cost=}')

if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
