# Process time: 1.98 seconds.
import functools
import operator
import time
from collections import defaultdict


def parse_input(lines: list[str]) -> tuple[dict[str, set[str]], set[frozenset]]:
    network_map = defaultdict(set)
    initial_connections = set()
    for line in lines:
        pc1, pc2 = line.split('-')
        network_map[pc1].add(pc2)
        network_map[pc2].add(pc1)
        initial_connections.add(frozenset({pc1, pc2}))
    return network_map, initial_connections


def add_one_to_lan(network_map: dict[str, set[str]], lans: set[frozenset]) -> set[frozenset]:
    """
    For a set of interconnected computers (a LAN), find any additional computers that are
    connected to all the computers. For any found, create a new LAN with one additional computer
    added. Return a list of new LANs
    """
    new_lans = set()
    for lan in lans:
        connections = {frozenset(network_map[computer]) for computer in lan}
        interconnected_computers = functools.reduce(operator.and_, connections)
        for new_computer in interconnected_computers:
            new_lans.add(frozenset({*lan, new_computer}))
    return new_lans


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    network_map, initial_connections = parse_input(lines)
    new_lans = add_one_to_lan(network_map, initial_connections)
    while len(new_lans) > 1:
        # Keep making LANs bigger until there is only one LAN.
        new_lans = add_one_to_lan(network_map, new_lans)

    password = ','.join(sorted(new_lans.pop()))
    print(password)


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
