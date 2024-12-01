import numpy as np
from pprint import pprint

fname = r'18/input.txt'
# fname = r'18/test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()
# print(lines)

# parse into list of dig_plan
direction_dict = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
dig_plan = [(direction_dict[line.strip()[-2]], int(line.strip()[-7:-2], 16)) for line in lines]
# print(dig_plan)

# find relevant coordinates (if we have an x coord of 10, we want to include columns 9, 10 and 11). Poss overkill.:
max_r = min_r = max_u = min_u = 0
horz = vert = 0
lr_coords = {horz}
ud_coords = {vert}
lagoon_coords = [(horz, vert)]
for direction, distance in dig_plan:
    if direction == 'R':
        horz += distance
    if direction == 'L':
        horz -= distance
    if direction == 'D':
        vert += distance
    if direction == 'U':
        vert -= distance
    lagoon_coords.append((horz, vert))
    # we want sets to contain one row/col either side of each corner coordinate
    lr_coords.update({horz - 1, horz, horz + 1})
    ud_coords.update({vert - 1, vert, vert + 1})


lr_encode = {original_value: transformed_value 
                  for transformed_value, original_value in enumerate(sorted(lr_coords))}
ud_encode = {original_value: transformed_value 
                  for transformed_value, original_value in enumerate(sorted(ud_coords))}

lr_decode = {key: val for val, key in lr_encode.items()}
ud_decode = {key: val for val, key in ud_encode.items()}

lr_widths = [1]
for i in range(1, len(lr_encode)):
    lr_widths.append(lr_decode[i] - lr_decode[i-1])

ud_widths = [1]
for i in range(1, len(ud_encode)):
    ud_widths.append(ud_decode[i] - ud_decode[i-1])

lagoon_encoding = np.outer(np.array(lr_widths), np.array(ud_widths))
# pprint(lagoon_encoding)

transformed_lagood_coords = [(lr_encode[horz], ud_encode[vert]) for horz, vert in lagoon_coords]
# pprint(transformed_lagood_coords)

lagoon = np.zeros_like(lagoon_encoding)

old_horz ,old_vert = transformed_lagood_coords[0]
for horz, vert in transformed_lagood_coords:
    if horz < old_horz or vert < old_vert:
        step = -1
    else:
        step = +1
    
    lagoon[old_horz: horz+step: step, old_vert: vert+step: step] = 1
    old_horz = horz
    old_vert = vert
# pprint(lagoon)

# Get coords of first point on top row (lagoon[1]; remember lagoon [0] is empty buffer). Going diagonally in should give us
# a seed point inside the trench.
seed_lr = np.where(lagoon[1] == 1)[0][0] + 1
seed_ud = 2

if lagoon[seed_ud][seed_lr] != 0:
    print(f'Error! invalid position {seed_ud=}, {seed_lr=}')
    exit(1)


points_to_check = {(seed_ud, seed_lr)}
while True:
    if not points_to_check:
        break  # stop when no points in set
    point_ud, point_lr = points_to_check.pop()
    if lagoon[point_ud, point_lr] > 0:
        continue

    lagoon[point_ud, point_lr] = 1
    points_to_check.add((point_ud+1, point_lr))
    points_to_check.add((point_ud-1, point_lr))
    points_to_check.add((point_ud, point_lr+1))
    points_to_check.add((point_ud, point_lr-1))

pprint(np.sum(np.multiply(lagoon, lagoon_encoding)))
