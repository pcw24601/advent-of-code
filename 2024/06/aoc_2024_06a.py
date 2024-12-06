from pprint import pprint
from typing import Tuple

fname = 'input.txt'
# fname='test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()
grid = [line.strip() for line in lines]

def rotate(grid: list[str]) -> list[str]:
    """Rotate grid -90 degrees"""
    rotated_grid = []
    num_rows = len(grid)
    num_cols = len(grid[0])
    for in_row_pos in range(num_rows):
        out_row = ''
        for in_col_pos in range(num_cols):
            out_row += grid[in_col_pos][num_rows - in_row_pos - 1]
        rotated_grid.append(out_row)
    return rotated_grid

def find_guard(grid: list[str]) -> tuple[int, int]:
    for rownum, row in enumerate(grid):
        col_pos = row.find('^')
        if col_pos >= 0:
            return rownum, col_pos
    raise RuntimeError('Cannot find guard!')


grid = rotate(grid)  # easier to move guard to left than upwards
row, col = find_guard(grid)
while True:
    grid[row] = grid[row][:col] + 'X' + grid[row][col+1:]  # replace guard with 'X'
    if col == 0:
        grid[row] = grid[row][:col] + 'X' + grid[row][col+1:]
        break
    if grid[row][col-1] == '#':
        grid[row] = grid[row][:col] + '^' + grid[row][col+1:]
        grid = rotate(grid)
        row, col = find_guard(grid)
        continue
    if grid[row][col-1] == '.':
        grid[row] = grid[row][:col] + 'X' + grid[row][col+1:]
    col -= 1

answer = sum(map(lambda s: s.count('X'), grid))
print(f'{answer=}')

