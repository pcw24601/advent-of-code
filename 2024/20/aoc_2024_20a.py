# Process time: 64.5 seconds.
import time
from collections import defaultdict
from heapq import heappush, heappop
from pprint import pprint


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
                case 'E':
                    end_pos = (row_num, col_num)
                    points.add((row_num, col_num))

    original_runtime = dijknstra(points, start_node, end_pos)

    time_savings = defaultdict(int)
    for block in blocks:
        these_points = points.copy()
        these_points.add(block)
        this_time = dijknstra(these_points, start_node, end_pos)
        delta = original_runtime - this_time
        if delta >= 100:
            time_savings[delta] += 1
    pprint(time_savings)
    answer = sum(time_savings.values())
    print(f'{answer=}')

def dijknstra(points, start_node, end_pos):
    processed_points = dict()
    nodes_to_proces = []
    heappush(nodes_to_proces, start_node)
    run_time = None

    while nodes_to_proces:
        cost, row_num, col_num = heappop(nodes_to_proces)
        if (row_num, col_num) in processed_points:
            continue
        if (row_num, col_num) == end_pos:
            run_time = cost
            break
        for row_diff, col_diff in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
            if (row_num + row_diff, col_num + col_diff) in points:
                heappush(nodes_to_proces, (cost + 1, row_num + row_diff, col_num + col_diff))
        processed_points[(row_num, col_num)] = cost

    return run_time


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
