import re
from pprint import pprint


fname = r'14/input.txt'
# fname = r'14/test.txt'

target_number_cycles = 1000000000


def rotate(input_list):
    # Flip horizontally then transpose => 90 deg rotation
    input_list = list(input_list)
    input_list.reverse()
    dim_1 = len(input_list)
    dim_2 = len(input_list[0])  # assume all same length

    output_list = []
    for x in range(dim_2):
        output_list.append("")
        for y in range(dim_1):
            output_list[x] += input_list[y][x]
    return output_list
# TEST:
# pprint(rotate(("abc", "def", "ghi")))

def roll_line_to_side(input_str):
    this_str, *other_str = input_str.split('#', maxsplit=1)
    num_O = this_str.count('O')
    num_dot = this_str.count('.')
    new_str = 'O' * num_O + '.' * num_dot
    if len(other_str) > 0:
        new_str += '#' + roll_line_to_side(other_str[0])
    return new_str
        
def roll_all_to_side(input_list):
    new_list = []
    for line in input_list:
        new_list.append(roll_line_to_side(line))
    return new_list
    

def score_line(input_str):
    input_str = input_str[-1::-1]  # reverse string
    matches = re.finditer('O', input_str)
    score = sum([match_.end() for match_ in matches])
    return score


def score_list(input_list):
    score = 0
    for ln in input_list:
        score += score_line(ln)
    return score


def cycle(input_list):
    for _ in range(4*1):
        input_list = roll_all_to_side(input_list)
        input_list = rotate(input_list)
    return tuple(input_list)


input_list = []
with open(fname, 'r') as fp:
    while ln:=fp.readline():
        input_list.append(ln.strip())
input_list = input_list
# pprint(input_list)


for _ in range(3):  # rotate N to right hand side
    input_list = tuple(rotate(input_list))


# Work onm the basis that input states will repeat themselves. If we find the start and end point of the repeating cycle,
# we can figure out the positions (and therefore score) at any time.
state_dict = {}
cycle_number = 0
while True:
    state_dict[input_list] = dict(cycle=cycle_number, score=score_list(input_list))
    input_list = cycle(input_list)
    cycle_number += 1
    if input_list in state_dict.keys():
        break
print(f'Previous cycle = {state_dict[input_list]} , this cycle number = {cycle_number}')

cycle_entry_point = state_dict[input_list]['cycle']
cycle_lengh = cycle_number - cycle_entry_point

reduced_cycle_number = ((target_number_cycles - cycle_entry_point) % cycle_lengh) + cycle_entry_point
for cycle_detail_dict in state_dict.values():
    if cycle_detail_dict['cycle'] == reduced_cycle_number:
        print(cycle_detail_dict['score'])
# print(state_dict[reduced_cycle_number])

# pprint(rotate(input_list))  # display with N up
