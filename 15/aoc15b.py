from pprint import pprint
from collections import OrderedDict

fname = r'15/input.txt'
# fname = r'15/test.txt'

def hash_label(label):
    hash_val = 0
    for char in label:
        hash_val += ord(char)
        hash_val *= 17
        hash_val %= 256
        # print(this_val)
    return hash_val

with open(fname, 'r') as fp:
    input_seq = fp.read().strip()

input_list = input_seq.split(',')
lens_boxes = {i: OrderedDict() for i in range(256)}

for ln in input_list:
    ln_list = ln.strip('-').split('=')
    lens_label = ln_list[0]
    box_number = hash_label(lens_label)

    if len(ln_list) == 2:
        # assignment
        lens_boxes[box_number][lens_label] = int(ln_list[1])

    else:
        # replacement
        try:
            del lens_boxes[box_number][lens_label]
        except KeyError:
            pass

# pprint(lens_boxes)

total_power = 0
for box_num, box in lens_boxes.items():
    for lens_pos, lens_power in enumerate(box.values()):
        this_power = (1 + box_num) * (lens_pos + 1) * lens_power
        total_power += this_power

print(total_power)