import re

fname = r'08/input.txt'
# fname = r'08/test.txt'


def follow_path(graph, path, step_count=0, current_point='AAA'):
    while True:
        for lr in path:
            if current_point == 'ZZZ':
                return step_count
            if lr == 'L':
                step_count += 1
                current_point = graph[current_point][0]
            elif lr == 'R':
                step_count += 1
                current_point = graph[current_point][1]
            # else:
            #     print('Error')
            #     return


with open(fname, 'r') as fp:
    path = fp.readline()
    fp.readline()  # discard empty line

    graph = {}
    while ln:=fp.readline():
        matches = re.match(r'(\w{3}) = \((\w{3}), (\w{3})\)', ln)
        graph[matches.group(1)] = (matches.group(2), matches.group(3))
        # for i in range(4):
        #     print(matches.group(i))
print(follow_path(graph, path))
# print(graph)

