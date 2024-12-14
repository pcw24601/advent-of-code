# Process time: 0.136 seconds.
import re
import time
from typing import Iterable, Optional


def parse_input(lines: str) -> Iterable:
    machine_details = re.findall(
        r'Button A: X([\+\-]?\d+), Y([\+\-]?\d+)\n'
        r'Button B: X([\+\-]?\d+), Y([\+\-]?\d+)\n'
        r'Prize: X=([\+\-]?\d+), Y=([\+\-]?\d+)',
        lines
    )
    machine_details = map(lambda tuple_: tuple(int(s) for s in tuple_), machine_details)
    return machine_details


def process_machine(machine_details: tuple[int, int, int, int, int, int]) -> Optional[int]:
    ax, ay, bx, by, px, py = machine_details
    # max_a = min(px // ax, py // ay)
    # max_b = min(px // bx, py // by)
    cost = None
    for a_press in range(101):
        for b_press in range(101):
            if (ax * a_press + bx * b_press == px) and (ay * a_press + by * b_press == py):
                if cost is None:
                    cost = a_press * 3 + b_press
                else:
                    cost = min(cost, a_press * 3 + b_press)
    return cost


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read()

    machine_details = parse_input(lines)
    machine_costs = map(process_machine, machine_details)
    answer = 0
    for cost in machine_costs:
        if cost:
            answer += cost

    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
