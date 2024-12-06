import copy

fname = 'input.txt'
# fname='test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()
grid = [list(line.strip()) for line in lines]

def find_guard(grid: list[list[str]]) -> tuple[int, int]:
    for row_pos, row in enumerate(grid):
        for col_pos, object in enumerate(row):
            if object == '^':
                return row_pos, col_pos
    raise RuntimeError('Cannot find guard!')

num_rows = len(grid)
num_cols = len(grid[0])


def direction():
    while True:
        yield -1, 0
        yield 0, 1
        yield 1, 0
        yield 0, -1


class GridExit(Exception):
    pass


def make_move(grid, row_pos, col_pos, row_dir, col_dir):
    # returns end position and direction
    while True:
        next_row = row_pos + row_dir
        next_col = col_pos + col_dir

        if not ((0 <= next_row < num_rows) and (0 <= next_col < num_cols)):
            raise GridExit  # Not a loop
        next_object = grid[next_row][next_col]
        if next_object in ['.', '^']:
            row_pos, col_pos = next_row, next_col
        elif next_object == '#':
            return row_pos, col_pos, row_dir, col_dir


initial_guard_pos = find_guard(grid)
answer = 0

for obstacle_row in range(num_rows):
    for obstacle_col in range(num_cols):
        if grid[obstacle_row][obstacle_col] != '.':
            continue
        this_grid = copy.deepcopy(grid)
        this_grid[obstacle_row][obstacle_col] = '#'
        direction_gen = direction()
        row_dir, col_dir = next(direction_gen)
        loop_set = set()
        row_pos, col_pos = initial_guard_pos
        try:
            while True:
                row_pos, col_pos, row_dir, col_dir = make_move(
                    this_grid, row_pos, col_pos, row_dir, col_dir)
                if (row_pos, col_pos, row_dir, col_dir) in loop_set:
                    answer += 1
                    break
                loop_set.add((row_pos, col_pos, row_dir, col_dir))
                row_dir, col_dir = next(direction_gen)
        except GridExit:
            pass

print(f'{answer=}')
