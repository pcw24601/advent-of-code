fname = 'input.txt'
# fname='test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()
grid = [line.strip() for line in lines]

mas_count = 0
for row, line in enumerate(grid[:-1]):
    # looking for 'A'--can't be in first or last row
    if row == 0:
        continue
    for col_pos, letter in enumerate(line[:-1]):
        # looking for 'A'--can't be in first or last col
        if col_pos == 0:
            continue
        if letter == 'A':
            set1 = {
                grid[row + 1][col_pos + 1],
                grid[row - 1][col_pos - 1],
            }
            set2 = {
                grid[row - 1][col_pos + 1],
                grid[row + 1][col_pos - 1],
            }
            mas_count += (set1 == set2 == {'M', 'S'})

print(mas_count)
