fname = 'input.txt'
# fname='test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()
lines = [line.strip() for line in lines]

def rotate(grid: list[str]) -> list[str]:
    """Rotate grid 90 degrees"""
    rotated_grid = []
    num_rows = len(grid)
    num_cols = len(grid[0])
    for in_row_pos in range(num_rows):
        out_row = ''
        for in_col_pos in range(num_cols):
            out_row += grid[num_cols-in_col_pos-1][in_row_pos]
        rotated_grid.append(out_row)
    return rotated_grid

def diagonalise(grid: list[str]) -> list[str]:
    """Rotate grid 45 degrees"""
    diagonalised_grid = []
    for start_row in range(len(grid)):
        this_row = start_row
        this_col = 0
        out_row = ''
        while True:
            try:
                out_row += grid[this_row][this_col]
                this_col += 1
                this_row += 1
            except IndexError:
                # We've used up everything in that diagonal
                break
        diagonalised_grid.append(out_row)
    for start_col in range(1, len(grid[0])):  # omit col=0 as this repeats row=0
        this_row = 0
        this_col = start_col
        out_row = ''
        while True:
            try:
                out_row += grid[this_row][this_col]
                this_col += 1
                this_row += 1
            except IndexError:
                # We've used up everything in that diagonal
                break
        diagonalised_grid.append(out_row)
    return diagonalised_grid


def count_xmas_samx(lines: list[str]) -> int:
    """Count matches for a column"""
    xmas_count = 0
    for line in lines:
        xmas_count += line.count('XMAS') + line.count('SAMX')
    return xmas_count


xmas_count = count_xmas_samx(lines)
xmas_count += count_xmas_samx(rotate(lines))
xmas_count += count_xmas_samx(diagonalise(lines))
xmas_count += count_xmas_samx(diagonalise(rotate(lines)))

print(xmas_count)
