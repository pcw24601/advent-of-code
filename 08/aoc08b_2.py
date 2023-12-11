"""
Earlier version of code. This should get the correct answer, but, after a few itterations, 
the estimated run time is 24h.
"""

import re
from pprint import pprint
from collections import Counter
from time import process_time

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
        

ptime_start = process_time()

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

loop_number = 0
while True:
    list_of_zsets = []
    new_node_list = []
    for node in node_list:
        new_node_list.append(summary_graph[node]['end_node'])
        list_of_zsets.append(summary_graph[node]['z_indicies_set'])
    intersect = list_of_zsets[0].intersection(*list_of_zsets[1:])
    if len(intersect) > 0:
        steps = loop_number * steps_per_loop + min(intersect)
        print(f'{steps=} {loop_number=} {intersect=}')
        break
    loop_number += 1
    node_list = new_node_list

    if loop_number % 1e8 == 0:
        steps = loop_number * steps_per_loop
        ptime = process_time() - ptime_start
        print(f'{loop_number= }  {steps=}  {ptime=}')


