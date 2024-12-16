# Process time: 0.0259 seconds.
import time


class MoveBlocked(Exception):
    ...


def parse_grid(grid_str):
    grid = []
    for row_str in grid_str.split():
        row = []
        for char in row_str:
            match char:
                case 'O':
                    new_chars = '[]'
                case '@':
                    new_chars = '@.'
                case _:
                    new_chars = char * 2
            row += list(new_chars)
        grid.append(row)
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


def move_item_one_square(grid, item_row, item_col, move_symbol, previous_item='.', joined=False):
    item_symbol = grid[item_row][item_col]
    update_grid = {}
    moved_blocks = set()
    match move_symbol:
        case 'v':
            next_row, next_col = item_row + 1, item_col
        case '>':
            next_row, next_col = item_row, item_col + 1
        case '<':
            next_row, next_col = item_row, item_col - 1
        case '^':
            next_row, next_col = item_row - 1, item_col
        case _:
            raise RuntimeError
    match item_symbol:
        case '@':
            try:
                update_grid, moved_blocks, _, _ = move_item_one_square(grid, next_row, next_col,
                                                                       move_symbol,
                                                                       previous_item=item_symbol)
            except MoveBlocked:
                return {}, set(), item_row, item_col
        case '[':
            update_grid, moved_blocks, _, _ = move_item_one_square(grid, next_row, next_col,
                                                                move_symbol,
                                                                previous_item=item_symbol)
            if move_symbol in '^v' and not joined:
                second_grid, more_moved_blocks, _, _ = move_item_one_square(grid, item_row,
                                                                            item_col + 1,
                                                                            move_symbol,
                                                                            joined=True)
                update_grid.update(second_grid)
                moved_blocks.update(more_moved_blocks)
        case ']':
            update_grid, moved_blocks, _, _ = move_item_one_square(grid, next_row, next_col,
                                                                move_symbol,
                                                                previous_item=item_symbol)
            if move_symbol in '^v' and not joined:
                second_grid, more_moved_blocks, _, _ = move_item_one_square(grid, item_row,
                                                                            item_col - 1,
                                                                            move_symbol,
                                                                            joined=True)
                update_grid.update(second_grid)
                moved_blocks.update(more_moved_blocks)
        case '.':
            return update_grid, moved_blocks, next_row, next_col
        case '#':
            raise MoveBlocked
        case _:
            raise RuntimeError

    update_grid[(next_row, next_col)] = item_symbol
    moved_blocks.add((item_row, item_col))
    return update_grid, moved_blocks, next_row, next_col


def advance_grid(grid, grid_changes, moved_blocks):
    for row, col in moved_blocks:
        grid[row][col] = '.'
    for (row, col), item in grid_changes.items():
        grid[row][col] = item
    return grid


def score_grid(grid):
    score = 0
    for row_num, row in enumerate(grid):
        for col_num, char in enumerate(row):
            if char == '[':
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
        grid_updates, moved_blocks, robot_row, robot_col = move_item_one_square(grid, robot_row,
                                                                          robot_col,
                                                                  instruction)
        grid = advance_grid(grid, grid_updates, moved_blocks)
        # print('\n', instruction_number + 1, instruction)
        # display_grid(grid)
    # display_grid(grid)
    answer = score_grid(grid)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
