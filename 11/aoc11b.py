import re

fname = r'11/input.txt'
# fname = r'11/test.txt'

distance_factor = 1e6

with open(fname, 'r') as fp:
    input_list = fp.readlines()

original_coords = []

galaxy = re.compile('#')
for line_num, line in enumerate(input_list):
    matches = re.finditer(galaxy, line)
    original_coords.append([(line_num, match.start()) for match in matches])

# flatten list
original_coords = [coords for sublist in original_coords for coords in sublist]

row_numbers = set([coord[0] for coord in original_coords])  # rows with galaxies
col_numbers = set([coord[1] for coord in original_coords])  # cols with galaxies

# get empty rows / cols
max_row = max(row_numbers)
max_col = max(col_numbers)
empty_rows = set(range(max_row)) - row_numbers
empty_cols = set(range(max_col)) - col_numbers


# transform coordinates -- add (distance_factor - 1) on each axis for each empty row/col before that axis
new_coords = []
for coords in original_coords:
    transformed_coords = (
        coords[0] + (distance_factor - 1) * len(empty_rows - set(range(coords[0], max_row))),
        coords[1] + (distance_factor - 1) * len(empty_cols - set(range(coords[1], max_col)))
    )
    new_coords.append(transformed_coords)


# Find path length between galaxies
total_path = 0
for from_coord in new_coords:
    for to_coord in new_coords:  # will measure to self, but this will be zero
        this_path = abs(from_coord[0] - to_coord[0]) + abs(from_coord[1] - to_coord[1])
        total_path += this_path
        # print(f'{total_path=}  {this_path=}  {from_coord=}  {to_coord=}')


print(int(total_path/2))  # we counted each path twice

# print(match_coords)
# print(new_coords)
# print(f'{empty_cols=}  {empty_rows=}')