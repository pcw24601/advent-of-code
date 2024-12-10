# Process time: 0.00317 seconds.
import time


def find_trail(grid, num_rows, num_cols, current_pos):
    cur_row, cur_col = current_pos
    current_height = grid[cur_row][cur_col]
    if current_height == 9:
        return 1
    rating = 0
    for test_row, test_col in [
        (cur_row - 1, cur_col),
        (cur_row + 1, cur_col),
        (cur_row, cur_col - 1),
        (cur_row, cur_col + 1),
    ]:
        if (0 <= test_row < num_rows) and (0 <= test_col < num_cols):
            next_height = grid[test_row][test_col]
            if next_height == current_height + 1:
                rating += find_trail(grid, num_rows, num_cols, (test_row, test_col))
    return rating


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        grid = fp.read().splitlines()

    for row_num, line in enumerate(grid):
        grid[row_num] = list(map(int, line))

    num_rows = len(grid)
    num_cols = len(grid[0])

    start_positions = set()
    for row_num, row in enumerate(grid):
        for col_num, height in enumerate(row):
            if height == 0:
                start_positions.add((row_num, col_num))

    answer = sum(map(lambda pos: find_trail(grid, num_rows, num_cols, pos), start_positions))
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
