import re

fname = r'03/input.txt'
# fname = r'03/test.txt'

sum = 0
schematic = []

with open(fname, 'r') as f:
    while ln:=f.readline():
        schematic.append(ln)
num_lines = len(schematic)
line_length = len(schematic[0])

for line_num, line in enumerate(schematic):
    symbols_iter = re.finditer('\*', line)

    for symbol_match in symbols_iter:
        part_nums = []
        for part_line_num in range(max(0, line_num-1), min(line_num+2, num_lines)):
            part_search_line = schematic[part_line_num]
            part_nums_matches = re.finditer('\d+', part_search_line)
            for part_num_match in part_nums_matches:
                if symbol_match.start() in range(part_num_match.start()-1, part_num_match.end()+1):
                    part_nums.append(int(part_num_match.group(0)))
        if len(part_nums) == 2:
            gear_ratio = part_nums[0] * part_nums[1]
            sum += gear_ratio

print(sum)