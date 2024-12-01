import re
from pprint import pprint

fname = r'10/input.txt'
# fname = r'10/test2.txt'

graph = {}
maze = []

line_num = 0
with open(fname, 'r') as fp:
    while ln:=fp.readline():
        maze.append(list(ln.strip()))
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
    (start_line, start_row + 1),  #0
    (start_line, start_row - 1),  #1
    (start_line + 1, start_row),  #2
    (start_line - 1, start_row)   #3
]

index_set = set()
for index_, check_node in enumerate(check_nodes):
    if check_node in graph.keys():
        if start_pos in graph[check_node]:
            this_node = check_node
            graph[start_pos].append(check_node)
            index_set.add(index_)

if index_set == {0,1}:
    maze[start_line][start_row] = '-'
elif index_set == {0,2}:
    maze[start_line][start_row] = 'F'
elif index_set == {0,3}:
    maze[start_line][start_row] = 'L'
elif index_set == {1,2}:
    maze[start_line][start_row] = '7'
elif index_set == {1,3}:
    maze[start_line][start_row] = 'J'
elif index_set == {2,3}:
    maze[start_line][start_row] = '|'
else:
    print(f'Invalid {index_set=}')

# for maze_line in maze:
#     for char in maze_line:
#         print(char, end='')
#     print()

print(f'{graph[start_pos]=}')

number_steps = 0
last_node = this_node
this_node = start_pos
next_node = None
while next_node != start_pos:
    this_char = maze[this_node[0]][this_node[1]]
    if this_char in "|JL":
        maze[this_node[0]][this_node[1]] = 'X' # Changes inside / outside loop
    elif this_char in "-7F":
        maze[this_node[0]][this_node[1]] = 'Z'  # Don't change inside / outside loop, nor add to inside area

    next_node = graph[this_node][0]
    if next_node == last_node:
        next_node = graph[this_node][1]
    number_steps += 1
    last_node, this_node = this_node, next_node

print(number_steps / 2)

inside_loop = False
loop_area = 0
for line_num in range(len(maze)):
    for char_num in range(len(maze[line_num])):
        char = maze[line_num][char_num]
        if char == 'X':
            inside_loop = inside_loop ^ True  # XOR, flip inside_loop
        elif char != 'Z':
            if inside_loop:
                loop_area += 1
                maze[line_num][char_num] = '@'


print(loop_area) 
# for maze_line in maze:
#     for char in maze_line:
#         print(char, end='')
#     print()
