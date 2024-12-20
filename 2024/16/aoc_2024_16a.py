# Process time: 0.221 seconds.
import time
from dataclasses import dataclass, field
from heapq import heappush, heappop

TURN_COST = 1000


@dataclass(frozen=True, order=True)
class Node:
    cost_estimate: int
    actual_cost: int
    row: int = field(compare=False)
    col: int = field(compare=False)
    direction: str = field(compare=False)

    @property
    def coords(self):
        return self.row, self.col

    @property
    def turn_directions(self):
        match self.direction:
            case 'u' | 'd':
                return 'lr'
            case 'r' | 'l':
                return 'ud'

    @property
    def search_id(self):
        return self.row, self.col, self.direction


def create_node(pos: tuple[int, int], direction: str, end_pos: tuple[int, int],
                current_cost: int) -> Node:
    row, col = pos
    end_row, end_col = end_pos
    l1_distance = abs(row - end_row) + abs(col - end_col)
    rotation_cost = 0
    if end_row > row and direction != 'r':
        rotation_cost += TURN_COST
    if end_row < row and direction != 'l':
        rotation_cost += TURN_COST
    if end_col > col and direction != 'u':
        rotation_cost += TURN_COST
    if end_col < col and direction != 'd':
        rotation_cost += TURN_COST
    cost_estimate = current_cost + l1_distance + rotation_cost
    return Node(cost_estimate=cost_estimate, actual_cost=current_cost,
                row=row, col=col, direction=direction)


def parse_input(lines):
    node_coords = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            match char:
                case '.':
                    node_coords.add((row, col))
                case 'S':
                    start_pos = (row, col)
                case 'E':
                    end_pos = (row, col)
                    node_coords.add((row, col))  # make end a node
    return node_coords, start_pos, end_pos


def generate_search_nodes(current_node: Node,
                          nodes_to_search: list[Node],
                          end_pos: tuple[int, int],
                          searched_node_ids: set[tuple[int, int, str]],
                          all_nodes: set[tuple[int, int]]):
    move_dir = dict(
        l=(0, -1),
        r=(0, 1),
        u=(-1, 0),
        d=(1, 0),
    )
    new_row = current_node.row + move_dir[current_node.direction][0]
    new_col = current_node.col + move_dir[current_node.direction][1]
    new_node = create_node((new_row, new_col), current_node.direction, end_pos,
                           current_node.actual_cost + 1)
    if (new_node.search_id not in searched_node_ids) and (new_node.coords in all_nodes):
        heappush(nodes_to_search, new_node)

    for new_dir in current_node.turn_directions:
        new_node = create_node(current_node.coords, new_dir, end_pos,
                               current_node.actual_cost + TURN_COST)
        if new_node.search_id not in searched_node_ids:
            heappush(nodes_to_search, new_node)


def a_star_search(nodes_to_search: list[Node],
                  end_pos: tuple[int, int],
                  all_nodes: set[tuple[int, int]]) -> int:
    searched_node_ids: set[tuple[int, int, str]] = set()
    while nodes_to_search:
        this_node = heappop(nodes_to_search)
        if this_node.search_id in searched_node_ids:
            continue
        if this_node.coords == end_pos:
            return this_node.actual_cost
        searched_node_ids.add(this_node.search_id)
        generate_search_nodes(this_node, nodes_to_search, end_pos, searched_node_ids, all_nodes)


def main():
    fname = 'input.txt'
    # fname = 'test2.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    node_coords, start_pos, end_pos = parse_input(lines)
    start = create_node(start_pos, 'r', end_pos, 0)
    nodes_to_search = []
    heappush(nodes_to_search, start)

    answer = a_star_search(nodes_to_search, end_pos, node_coords)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
