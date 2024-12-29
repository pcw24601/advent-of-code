# Process time: 9.6 seconds.
import time
from collections import defaultdict
from heapq import heappush, heappop
from itertools import product
from pprint import pprint


def good_cheat(node1: tuple[int, int, int], node2: tuple[int, int, int]) -> bool:
    max_cheat_time = 20
    good_cheat_threshold = 100
    t1, row1, col1 = node1
    t2, row2, col2 = node2

    l1_dist = abs(row1 - row2) + abs(col1 - col2)
    if l1_dist > max_cheat_time:
        # Cheat distance too big
        return False
    if (t2 - t1) - l1_dist >= good_cheat_threshold:
        # Cheat saves enough time
        return True
    # Cheat won't save enough time
    return False


def find_total_savings(node_set):
    total_savings = sum(map(lambda node_tuple: good_cheat(*node_tuple), product(node_set,
                                                                                repeat=2)))
    return total_savings


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    points = set()
    blocks = set()
    for row_num, line in enumerate(lines):
        for col_num, char in enumerate(line):
            match char:
                case '.':
                    points.add((row_num, col_num))
                case '#':
                    if (0 < row_num < len(lines) - 1) and (0 < col_num < len(line) + 1):
                        blocks.add((row_num, col_num))
                case 'S':
                    start_node = (0, row_num, col_num)  # cost, row_num, col_num
                    points.add((row_num, col_num))
                case 'E':
                    end_pos = (row_num, col_num)
                    points.add((row_num, col_num))

    non_cheat_node_time = dijknstra(points, start_node, end_pos)


    answer = find_total_savings(non_cheat_node_time)
    print(f'{answer=}')

def dijknstra(points, start_node, end_pos):
    processed_points = dict()
    processed_set = set()
    nodes_to_proces = []
    heappush(nodes_to_proces, start_node)
    run_time = None

    while nodes_to_proces:
        cost, row_num, col_num = heappop(nodes_to_proces)
        if (row_num, col_num) in processed_points:
            continue
        processed_points[(row_num, col_num)] = cost
        processed_set.add((cost, row_num, col_num))
        if (row_num, col_num) == end_pos:
            run_time = cost
            break
        for row_diff, col_diff in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
            if (row_num + row_diff, col_num + col_diff) in points:
                heappush(nodes_to_proces, (cost + 1, row_num + row_diff, col_num + col_diff))

    return processed_set


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
