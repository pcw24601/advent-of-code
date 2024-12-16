# Process time: 0.0137 seconds.
import time


class MoveBlocked(Exception):
    ...


def parse_grid(grid_str):
    grid = [[c for c in line] for line in grid_str.split('\n')]
    return grid


def display_grid(grid):
    for row in grid:
        for char in row:
            print(char, end='')
        print()


def find_robot(grid):
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            if char == r'@':
                return row_num, col_num
    raise RuntimeError('Robot not found')


def move_item_one_square(grid, item_row, item_col, move_symbol, previous_item='.'):
    item_symbol = grid[item_row][item_col]
    match move_symbol:
        case 'v':
            next_row, next_col = item_row + 1, item_col
        case '>':
            next_row, next_col = item_row, item_col + 1
        case '<':
            next_row, next_col = item_row, item_col - 1
        case '^':
            next_row, next_col = item_row - 1, item_col
    match item_symbol:
        case '@':
            try:
                grid, _, _ = move_item_one_square(grid, next_row, next_col, move_symbol,
                                                  previous_item=item_symbol)
            except MoveBlocked:
                return grid, item_row, item_col
            grid[next_row][next_col] = item_symbol
            grid[item_row][item_col] = previous_item

        case 'O':
            grid, _, _ = move_item_one_square(grid, next_row, next_col, move_symbol,
                                              previous_item=item_symbol)
            grid[next_row][next_col] = item_symbol
            grid[item_row][item_col] = previous_item
        case '.':
            pass
        case '#':
            raise MoveBlocked
        case _:
            raise RuntimeError
    return grid, next_row, next_col


def score_grid(grid):
    score = 0
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            if char == 'O':
                score += 100 * row_num + col_num
    return score


def main():
    fname = 'input.txt'
    # fname = 'test2.txt'
    # fname = 'test1.txt'

    with open(fname, 'r') as fp:
        input = fp.read()

    grid_str, instruction_str = input.split('\n\n')
    grid = parse_grid(grid_str)

    robot_row, robot_col = find_robot(grid)

    instruction_str = instruction_str.replace('\n', '')

    for instruction_number, instruction in enumerate(instruction_str):
        grid, robot_row, robot_col = move_item_one_square(grid, robot_row, robot_col,
                                                          instruction)
    answer = score_grid(grid)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
