import numpy as np
from pprint import pprint

fname = r'18/input.txt'
# fname = r'18/test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()
# print(lines)

# parse into list of dig_plan, ignoring colours
dig_plan = [(line.split()[0], int(line.split()[1])) for line in lines]
# print(dig_plan)

# find maximum dimensions:
max_r = min_r = max_u = min_u = 0
horz = vert = 0
for direction, distance in dig_plan:
    if direction == 'R':
        horz += distance
        max_r = max(horz, max_r)
    if direction == 'L':
        horz -= distance
        min_r = min(horz, min_r)
    if direction == 'D':
        vert += distance
        max_u = max(vert, max_u)
    if direction == 'U':
        vert -= distance
        min_u = min(vert, min_u)
        
print(f'{min_r=} {max_r=} {min_u=} {max_u=}')

lagoon = np.zeros((max_u - min_u + 3, max_r - min_r + 3), dtype=int)  # Make first/last row and first/last col all zeroes to allow correct indexing
new_lr = current_lr = 1 - min_r
new_ud = current_ud = 1 - min_u
lagoon[current_ud, current_lr] = 1
# pprint(lagoon)

# new_ud = new_lr = 0
for direction, length in dig_plan:
    
    match direction:
        case 'U':
            new_ud = current_ud - length
            step = -1
        case 'D':
            new_ud = current_ud + length
            step = 1
        case 'R':
            new_lr = current_lr + length
            step = 1
        case 'L':
            new_lr = current_lr - length
            step = -1
    
    lagoon[current_ud: new_ud + step: step, current_lr: new_lr + step: step] = 1
    current_lr = new_lr
    current_ud = new_ud
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

    lagoon[point_ud, point_lr] = 2
    points_to_check.add((point_ud+1, point_lr))
    points_to_check.add((point_ud-1, point_lr))
    points_to_check.add((point_ud, point_lr+1))
    points_to_check.add((point_ud, point_lr-1))

# pprint(lagoon)

print(len(np.flatnonzero(lagoon)))