# Process time: 0.000823 seconds.
import time
from collections import defaultdict
from heapq import heappush, heappop
from itertools import pairwise


class Robot:
    position_map = {}  # Need to overwrite in subclass
    def __init__(self, parent_robot=None):
        self.row, self.col = self.position_map['A']
        self._create_cost_map(parent_robot)
        self._dijknstra()
        self.button_map = {}

    def _create_cost_map(self, parent_robot):
        if parent_robot is None:
            self.parent_cost_map = defaultdict(lambda: 1)
        else:
            self.parent_cost_map = parent_robot.cost_dict

    def _dijknstra(self):
        min_cost = {}
        # (start_symbol, end_symbol): cost to move from start_symbol to pressing end_symbol

        for start_row, start_col in self.button_map:
            checked_nodes = set()
            nodes_to_check = []
            start_node = (0, start_row, start_col, 'A', False)
            # cost, row, col, parent_loc, pressed?
            # parent_loc is the last button the parent robot pressed--this will affect the
            # shortest path
            heappush(nodes_to_check, start_node)
            start_symbol = self.button_map[(start_row, start_col)]
            while nodes_to_check:
                cost, row, col, parent_loc, pressed = heappop(nodes_to_check)
                if (row, col, parent_loc, pressed) in checked_nodes:
                    continue
                this_symbol = self.button_map[(row, col)]
                checked_nodes.add((row, col, parent_loc, pressed))
                if pressed:
                    min_cost[(start_symbol, this_symbol)] = cost
                    continue
                for row_diff, col_diff, new_pressed, parent_target in {
                    (1, 0, False, 'v'),
                    (-1, 0, False, '^'),
                    (0, 1, False, '>'),
                    (0, -1, False, '<'),
                    (0, 0, True, 'A'),
                }:
                    new_row, new_col = row + row_diff, col + col_diff
                    if (new_row, new_col) not in self.button_map:
                        continue
                    if (new_row, new_col, parent_target, new_pressed) in checked_nodes:
                        continue
                    move_cost = self.parent_cost_map[(parent_loc, parent_target)]
                    heappush(nodes_to_check,
                             (cost + move_cost, new_row, new_col, parent_target, new_pressed))
        self.cost_dict = min_cost

    def key_string_cost(self, key_string):
        cost = sum(map(lambda x: self.cost_dict[x], pairwise(key_string)))
        return cost


class DirectionRobot(Robot):
    button_map = {
        (0, 1): '^',
        (0, 2): 'A',
        (1, 0): '<',
        (1, 1): 'v',
        (1, 2): '>',
    }
    position_map = {v: k for k, v in button_map.items()}


class KeypadRobot(Robot):
    button_map = {
        (0, 0): '7',
        (0, 1): '8',
        (0, 2): '9',
        (1, 0): '4',
        (1, 1): '5',
        (1, 2): '6',
        (2, 0): '1',
        (2, 1): '2',
        (2, 2): '3',
        (3, 1): '0',
        (3, 2): 'A',
    }
    position_map = {v: k for k, v in button_map.items()}


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    robot3 = DirectionRobot()
    robot2 = DirectionRobot(robot3)
    robot1 = KeypadRobot(robot2)

    answer = 0
    for line in lines:
        this_cost = robot1.key_string_cost('A' + line)
        this_complexity = this_cost * int(line[:-1])
        # print(f'{line}: {this_cost=}, {this_complexity=}')
        answer += this_complexity
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
