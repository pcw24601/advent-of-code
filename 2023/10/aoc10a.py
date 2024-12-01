import re

fname = r'10/input.txt'
# fname = r'10/test.txt'

graph = {}

line_num = 0
with open(fname, 'r') as fp:
    while ln:=fp.readline():
        matches = re.finditer(r'[SF7JL\-|]', ln)
        for match in matches:
            this_pipe = match.group(0)
            this_pos = match.start()
            if this_pipe == 'F':
                links = [(line_num, this_pos + 1), (line_num + 1, this_pos)]
            if this_pipe == 'J':
                links = [(line_num, this_pos - 1), (line_num - 1, this_pos)]
            if this_pipe == r'|':
                links = [(line_num - 1, this_pos), (line_num + 1, this_pos)]
            if this_pipe == r'-':
                links = [(line_num, this_pos + 1), (line_num, this_pos - 1)]
            if this_pipe == '7':
                links = [(line_num, this_pos - 1), (line_num + 1, this_pos)]
            if this_pipe == 'L':
                links = [(line_num, this_pos + 1), (line_num - 1, this_pos)]

            
            if this_pipe == 'S':
                start_line, start_row = line_num, this_pos
                links = []
            
            graph[(line_num, this_pos)] = links
        line_num += 1

# find links from start position
start_pos = (start_line, start_row)
check_nodes = [
    (start_line, start_row + 1),
    (start_line, start_row - 1),
    (start_line + 1, start_row),
    (start_line - 1, start_row)
]

for check_node in check_nodes:
    if check_node in graph.keys():
        if start_pos in graph[check_node]:
            this_node = check_node
            break
            # graph[start_pos].append(check_node)
        # print(next_node)

number_steps = 1
last_node = start_pos
while this_node != start_pos:
    next_node = graph[this_node][0]
    if next_node == last_node:
        next_node = graph[this_node][1]
    number_steps += 1
    last_node, this_node = this_node, next_node

print(number_steps / 2)