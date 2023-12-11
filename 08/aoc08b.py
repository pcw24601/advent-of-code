import re
from pprint import pprint
from collections import Counter
import numpy as np

fname = r'08/input.txt'
# fname = r'08/test4.txt'


def get_z_indicies(graph, path, node):

    z_indicies = set()
    step_count = 0

    for lr in path:
        if lr == 'L':
            step_count += 1
            node = graph[node][0]
        elif lr == 'R':
            step_count += 1
            node = graph[node][1]

        if node[2] == 'Z':
            z_indicies.add(step_count)

    return (node, z_indicies)


def process_graph(graph, path):
    graph_summary = {}
    for start_node in graph.keys():
        end_node, z_indicies_set = get_z_indicies(graph, path, start_node)
        graph_summary[start_node] = dict(end_node=end_node,
                                         z_indicies_set=z_indicies_set)
    return graph_summary
        


with open(fname, 'r') as fp:
    path = fp.readline().strip()
    fp.readline()  # discard empty line

    graph = {}
    while ln:=fp.readline():
        matches = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', ln)
        graph[matches.group(1)] = (matches.group(2), matches.group(3))

summary_graph = process_graph(graph, path)
steps_per_loop = len(path)

node_list = []
for node in graph.keys():
    if node[2] == 'A':
        node_list.append(node)
    
# print(f'{steps_per_loop=}')
# print(f'{node_list=}')
steps_ = []
for node in node_list:
    loop_number = 0
    # print(f'{node=}')
    list_of_zsets = []
    list_of_start_nodes = [node]
    start_node = node
    while True:
        new_node = summary_graph[node]['end_node']
        # print(f'{new_node=}  {list_of_start_nodes=}')
        if new_node in list_of_start_nodes:
            break
        loop_number += 1
        list_of_zsets.append(summary_graph[node]['z_indicies_set'])
        list_of_start_nodes.append(new_node)
        node = new_node
    steps_.append(loop_number * steps_per_loop)
    # print(f'{loop_number=}')

print(steps_)
print(np.lcm.reduce(steps_))
