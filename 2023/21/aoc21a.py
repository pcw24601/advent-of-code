from pprint import pprint

fname = r'21/input.txt'
# fname = r'21/test.txt'

# Load input
with open(fname, 'r') as fp:
    lines = fp.readlines()

garden_coords = set()
for ln_num, ln in enumerate(lines):
    for char_num, char in enumerate(ln.strip()):
        if char == '.':
            garden_coords.add((ln_num, char_num))
        
        if char == 'S':
            start_pos = (ln_num, char_num)

garden_coords.add(start_pos)
visited_gardens = {start_pos}

for _ in range(64):  # take 64 steps
    gardens_this_step = set()
    for x, y in visited_gardens:  # go through each garden visited
        for new_coords in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]: # try one step in any direction
                if new_coords in garden_coords:  # is it a garden?
                    gardens_this_step.add(new_coords)  # mark it as visited
    visited_gardens=gardens_this_step

print(len(visited_gardens))


