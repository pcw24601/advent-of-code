import re

fname = r'03/input.txt'
# fname = r'03/test.txt'

sum = 0
schematic = []
symbol_pattern = re.compile(r'[^\.a-zA-Z\n\d]')

with open(fname, 'r') as f:
    while ln:=f.readline():
        schematic.append(ln)
num_lines = len(schematic)
line_length = len(schematic[0])

for line_num, line in enumerate(schematic):
    part_nums_iter = re.finditer('\d+', line)

    for part_num_match in part_nums_iter:
        part_num = int(part_num_match.group(0))
        # check for nearby symbol
        symbol_found = False
        for symbol_line_num in range(max(0, line_num-1), min(line_num+2, num_lines-1)):
            symbol_search_substring = schematic[symbol_line_num][max(part_num_match.start()-1, 0): min(part_num_match.end()+1, line_length-1)]
            if sym:=re.findall(symbol_pattern,symbol_search_substring):
                symbol_found = True
        if symbol_found:
            sum += part_num


print(sum)