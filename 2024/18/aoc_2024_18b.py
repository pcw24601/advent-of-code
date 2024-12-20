# Process time: N/A
import re
import time
from dataclasses import field, dataclass
from heapq import heappush, heappop


@dataclass(frozen=True, order=True)
class Node:
    cost: int
    row: int = field(compare=False)
    col: int = field(compare=False)

    @property
    def coords(self):
        return self.row, self.col


def parse_input(line: str):
    coord_list = re.findall(r'(\d+),(\d+)', line)
    coord_list = list(map(lambda x: (int(x[0]), int(x[1])), coord_list))
    return coord_list


def form_grid(max_grid):
    grid_nodes = set()
    for row in range(max_grid + 1):
        for col in range(max_grid + 1):
            grid_nodes.add((row, col))
    return grid_nodes


def remove_corrupt_nodes(nodes: set, coord_list: list):
    for coords in coord_list:
        nodes.remove(coords)


def generate_search_nodes(current_node: Node,
                          nodes_to_search: list[Node],
                          all_nodes: set[tuple[int, int]],
                          current_cost: int,
                          ):
    move_dirs = {(0, 1), (0, -1), (1, 0), (-1, 0)}
    for move_dir in move_dirs:
        new_row = current_node.row + move_dir[0]
        new_col = current_node.col + move_dir[1]
        new_node = Node(row=new_row, col=new_col, cost=current_cost + 1)

        if new_node.coords not in all_nodes:
            continue
        heappush(nodes_to_search, new_node)


def find_dist(end_pos: tuple[int, int],
              all_nodes: set[tuple[int, int]]
              ):
    searched_nodes = set()
    start_node = Node(row=0, col=0, cost=0)
    nodes_to_search = []
    heappush(nodes_to_search, start_node)
    while nodes_to_search:
        this_node = heappop(nodes_to_search)
        if this_node.coords in searched_nodes:
            continue
        if this_node.coords == end_pos:
            return this_node.cost
        searched_nodes.add(this_node.coords)
        generate_search_nodes(this_node, nodes_to_search, all_nodes, this_node.cost)


def main():
    fname = 'input.txt'; max_grid = 70
    num_to_remove = 2908  # <== found by manual binary(-ish) search
    # fname = 'test.txt'; max_grid = 6; num_to_remove = 21

    with open(fname, 'r') as fp:
        lines = fp.read()

    coord_list = parse_input(lines)
    nodes = form_grid(max_grid)
    remove_corrupt_nodes(nodes, coord_list[:num_to_remove])

    distance = find_dist((max_grid, max_grid), nodes)

    print(f'{distance=}  coords={coord_list[num_to_remove-1]}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
