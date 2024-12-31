# Process time: 0.00276 seconds.
import time
from collections import defaultdict


def parse_input(lines: list[str]) -> dict[str, set[str]]:
    network_map = defaultdict(set)
    for line in lines:
        pc1, pc2 = line.split('-')
        network_map[pc1].add(pc2)
        network_map[pc2].add(pc1)
    return network_map


def count_triplets(network_map):
    matching_sets = set()  # set of sets, e.g. {{ab, cd, ef}, {pq, rs, uv}, ...}
    for first_computer in network_map:
        if first_computer[0] != 't':
            continue
        for second_computer in network_map[first_computer]:
            for third_computer in network_map[second_computer]:
                if first_computer in network_map[third_computer]:
                    matching_sets.add(frozenset({first_computer, second_computer, third_computer}))
    return len(matching_sets)


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    network_map = parse_input(lines)
    answer = count_triplets(network_map)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
