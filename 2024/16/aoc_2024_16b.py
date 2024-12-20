# Process time: 0.309 seconds.
import time
from dataclasses import dataclass, field
from heapq import heappush, heappop
from typing import Optional

TURN_COST = 1000


@dataclass(frozen=True, order=True)
class Node:
    cost_estimate: int
    actual_cost: int
    row: int = field(compare=False)
    col: int = field(compare=False)
    direction: str = field(compare=False)
    parent_id: Optional[tuple[int, int, str]] = field(compare=False)

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
                current_cost, parent_node: Optional[Node]) -> Node:
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
    parent_id = None if parent_node is None else parent_node.search_id
    return Node(cost_estimate=cost_estimate, actual_cost=current_cost,
                row=row, col=col, direction=direction, parent_id=parent_id)


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
                          all_nodes: set[tuple[int, int]],
                          node_details):
    move_dir = dict(
        l=(0, -1),
        r=(0, 1),
        u=(-1, 0),
        d=(1, 0),
    )
    new_row = current_node.row + move_dir[current_node.direction][0]
    new_col = current_node.col + move_dir[current_node.direction][1]
    new_node = create_node((new_row, new_col), current_node.direction, end_pos,
                           current_node.actual_cost + 1, current_node)
    if (new_node.search_id not in searched_node_ids) and (new_node.coords in all_nodes):
        new_cost = new_node.actual_cost
        if new_node.search_id in node_details:
            existing_cost = node_details[new_node.search_id]['actual_cost']
            if new_cost == existing_cost:
                node_details[new_node.search_id]['parent_nodes'].add(new_node.parent_id)
            elif new_cost < existing_cost:
                heappush(nodes_to_search, new_node)
                node_details[new_node.search_id] = dict(actual_cost=new_cost,
                                                        parent_nodes={new_node.parent_id})
        else:
            heappush(nodes_to_search, new_node)
            node_details[new_node.search_id] = dict(actual_cost=new_cost,
                                                    parent_nodes={new_node.parent_id})

    for new_dir in current_node.turn_directions:
        new_node = create_node(current_node.coords, new_dir, end_pos,
                               current_node.actual_cost + TURN_COST, current_node)
        if new_node.search_id not in searched_node_ids:
            new_cost = new_node.actual_cost
            if new_node.search_id in node_details:
                existing_cost = node_details[new_node.search_id]['actual_cost']
                if new_cost == existing_cost:
                    node_details[new_node.search_id]['parent_nodes'].add(new_node.parent_id)
                elif new_cost < existing_cost:
                    heappush(nodes_to_search, new_node)
                    node_details[new_node.search_id] = dict(actual_cost=new_cost,
                                                            parent_nodes={new_node.parent_id})
            else:
                heappush(nodes_to_search, new_node)
                node_details[new_node.search_id] = dict(actual_cost=new_cost,
                                                        parent_nodes={new_node.parent_id})


def a_star_search(nodes_to_search: list[Node],
                  end_pos: tuple[int, int],
                  all_nodes: set[tuple[int, int]],
                  node_details: dict[tuple[int, int, str], dict]) -> tuple[int, set[Node]]:
    searched_node_ids: set[tuple[int, int, str]] = set()
    final_cost = None
    final_nodes = set()
    while nodes_to_search:
        this_node = heappop(nodes_to_search)
        new_cost = this_node.actual_cost
        if this_node.search_id in searched_node_ids:
            current_cost = node_details[this_node.search_id]['actual_cost']
            if current_cost == this_node.actual_cost:
                node_details[this_node.search_id]['parent_nodes'].add(this_node.parent_id)
            if current_cost > this_node.actual_cost:
                print('Should not get here')
                node_details[this_node.search_id]=dict(actual_cost=new_cost,
                                                       parent_nodes={this_node.parent_id})
            continue
        try:
            current_cost = node_details[this_node.search_id]['actual_cost']
            if current_cost == this_node.actual_cost:
                node_details[this_node.search_id]['parent_nodes'].add(this_node.parent_id)
            if this_node.actual_cost < current_cost:
                node_details[this_node.search_id] = dict(actual_cost=new_cost,
                                                         parent_nodes={this_node.parent_id})
        except KeyError:
            node_details[this_node.search_id] = dict(actual_cost=new_cost,
                                                     parent_nodes={this_node.parent_id})

        if this_node.coords == end_pos:
            if not final_cost:
                final_cost = this_node.actual_cost
                final_nodes.add(this_node)
            if this_node.actual_cost == final_cost:
                # Keep searching until final cost increases
                final_nodes.add(this_node)
            else:
                return final_cost, final_nodes
        searched_node_ids.add(this_node.search_id)
        generate_search_nodes(this_node, nodes_to_search, end_pos, searched_node_ids, all_nodes,
                              node_details)

16

def count_good_seats(this_node_id, node_details):
    if this_node_id is None:
        return set()
    good_seat_coord_set = {this_node_id[0:2]}
    for parent in node_details[this_node_id]['parent_nodes']:
        good_seat_coord_set |= count_good_seats(parent, node_details)
    return good_seat_coord_set


def main():
    fname = 'input.txt'
    # fname = 'test2.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    node_coords, start_pos, end_pos = parse_input(lines)
    start = create_node(start_pos, 'r', end_pos, 0, None)
    node_details = {start.search_id: dict(actual_cost=0, parent_nodes=set())}
    nodes_to_search = []
    heappush(nodes_to_search, start)

    score, final_nodes = a_star_search(nodes_to_search, end_pos, node_coords, node_details)
    good_seat_set = set()
    for node in final_nodes:
        good_seat_set |= count_good_seats(node.search_id, node_details)

    print(f'{len(good_seat_set)=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
