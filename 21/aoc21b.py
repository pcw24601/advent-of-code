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
max_x = ln_num + 1
max_y = char_num + 1

garden_coords.add(start_pos)
visited_gardens = {start_pos}
processed_gardens = set()
possible_end_gardens = set()
num_steps = 26501365

for step_num in range(num_steps):  # take 64 steps
    if step_num % 10000 == 0:
        print(f'{step_num=}')
    gardens_this_step = set()
    for x, y in visited_gardens:  # go through each garden visited
        for new_coords in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]: # try one step in any direction
                new_x, new_y = new_coords
                if (new_x % max_x, new_y % max_y) in garden_coords:  # is it a garden?
                    if new_coords not in processed_gardens:
                        gardens_this_step.add(new_coords)  # mark it as visited
    processed_gardens.update(gardens_this_step)
    if step_num % 2 != num_steps % 2:
        possible_end_gardens.update(gardens_this_step)
    visited_gardens = gardens_this_step


# need to account for parity of visited gardens
print(len(possible_end_gardens))


