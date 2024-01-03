from pprint import pprint
from collections import defaultdict
import re

# Full version
fname = r'25/input.txt'
# delete verticies identified from graphviz
verticies_to_cut = [('hxq', 'txl'),
                    ('rtt', 'zcj'),
                    ('tpn', 'gxv')]

# # Test
# fname = r'25/test.txt'
# # delete verticies identified from graphviz
# verticies_to_cut = [('hfx', 'pzl'),
#                     ('bvb', 'cmg'),
#                     ('nvd', 'jqt')]


with open(fname, 'r') as fp:
    lines = fp.readlines()
# print(lines)
    
nodes = set()
graph = defaultdict(list)

for ln in lines:
    node1, *other_nodes = ln.strip().replace(':','').split()
    nodes.add(node1)
    for node2 in other_nodes:
        nodes.add(node2)
        graph[node1].append(node2)
        graph[node2].append(node1)

for node1, node2 in verticies_to_cut:
    graph[node1].remove(node2)
    graph[node2].remove(node1)


searched_nodes = set()
def find_linked_nodes(node):
    if node in searched_nodes:
        return
    searched_nodes.add(node)
    for linked_node in graph[node]:
        find_linked_nodes(linked_node)

find_linked_nodes(verticies_to_cut[0][0])
unsearched_nodes = nodes - searched_nodes

# print(searched_nodes, unsearched_nodes)
print(f'{len(searched_nodes)=}\n{len(unsearched_nodes)=}\nProduct= {len(searched_nodes)*len(unsearched_nodes)}')
