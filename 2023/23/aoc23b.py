from pprint import pprint
from collections import namedtuple, defaultdict
from typing import Optional
from copy import deepcopy
import time


start_time = time.time()
fname = r'23/input.txt'
fgraphname = r'23/graph.dot'

# fname = r'23/test.txt'
# fgraphname = r'23/test_graph.dot'

with open(fname, 'r') as fp:
    trail_map = fp.readlines()

graph = defaultdict(set)

process_list = [((0,1), (1,1))]  # list of nodes to process, along with next node direction
processed_nodes = {(0,1)}

def follow_to_next_node(current_point, next_point, path_length):
    # How many directions can we go? 
    # If only 1, follow it
    # If >1, define a new node
    # If on last line, define as node and return.
    cur_row, cur_col = current_point
    path_length += 1
    next_row, next_col = next_point
    if next_row == len(trail_map) - 1:
        # We're at the end point
        return (next_point, path_length, set())
    
    if next_row == 0:
        # We're back at the start
        return (next_point, path_length, set())

    check_coords = {(next_row + 1, next_col),
                    (next_row - 1, next_col),
                    (next_row, next_col + 1),
                    (next_row, next_col - 1)
                    }
    check_coords.discard(current_point)  # don't retrace steps

    possible_points = set()
    forest_count = 0
    for row, col in check_coords:
        next_pos = trail_map[row][col]
        if next_pos == '#':
            # if not exactly 2, then its a node
            forest_count += 1  
        if next_pos in '.><^v':
            possible_points.add((row, col))
     
    if forest_count < 2:
        # at a node
        # possible_points.add(current_point)  # check for reverse path
        return (next_point, path_length, possible_points)
    
    if len(possible_points) == 1:
        return follow_to_next_node(next_point, possible_points.pop(), path_length)
    
    print('Error, should never get here')

while True:
    if not len(process_list):
        break
    this_node, next_point = process_list.pop()
    if this_node[0] == len(trail_map) - 1:
        continue
    next_node, path_length, next_points_set = follow_to_next_node(this_node, next_point, 0)
    graph[this_node].add((next_node, path_length))
    graph[next_node].add((this_node, path_length)) # add reverse path
    if next_node not in processed_nodes:
        # search other directions
        for next_point in next_points_set:
            process_list.append((next_node, next_point))
        processed_nodes.add(next_node)

# pprint(graph)

max_row = len(trail_map)  # get coord of exit point

def search_graph(graph: dict, searched_nodes: set, this_node: tuple) -> Optional[int]:
    if this_node in searched_nodes:
        return None
    
    if this_node[0] == max_row-1:
        # At exit point
        return 0
    searched_nodes.add(this_node)

    path_length_list = []
    # Otherwise add path length and search
    for search_node, edge_length in graph[this_node]:
        path_length = search_graph(graph, deepcopy(searched_nodes), search_node)
        if path_length is not None:
            path_length_list.append(edge_length + path_length)
    
    if path_length_list:
        # Is there a route to the exit? ...yes, return length
        return(max(path_length_list))
    # ...no, return None
    return None

print(search_graph(graph, set(), (0,1)))


# Visaulisation routine. Turns out, not that useful. Best plotted with `neato`
# Write graph to graphviz dot format
# def node_id(node):
#     return f'n{node}'.replace('(', '').replace(')', '').replace(', ', '_')
#
# with open(fgraphname, 'w') as fp:
#     fp.write('strict graph trail_route {\n')
#     # write nodes
#     for i, node in enumerate(graph):
#         node_str = node_id(node)
#         fp.write(f'    {node_str} [label="{node_str}"];\n')
#     # write edges
#     fp.write('    # Edges\n')
#     for node, val in graph.items():
#         from_node_str = node_id(node)
#         for to_node, path_length in val:
#             fp.write(f'    {from_node_str} -- {node_id(to_node)} [label="{path_length}"]\n')
#             # fp.write(f'    {from_node_str} -- {node_id(to_node)}\n')
#     # Tidy up
#     fp.write('}\n')

end_time = time.time()

print(f'{end_time-start_time=}')
# time = 2835 seconds (47 mins)