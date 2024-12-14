# Process time: 0.00429 seconds.
import re
import time
from fractions import Fraction
from typing import Iterable, Optional


def parse_machine(machine_details: tuple[int, int, int, int, int, int]):
    return tuple(
        int(s) if pos <= 3 else int(s) + int(1e13) for pos, s in enumerate(machine_details)
    )


def parse_input(lines: str) -> Iterable:
    machine_details = re.findall(
        r'Button A: X([\+\-]?\d+), Y([\+\-]?\d+)\n'
        r'Button B: X([\+\-]?\d+), Y([\+\-]?\d+)\n'
        r'Prize: X=([\+\-]?\d+), Y=([\+\-]?\d+)',
        lines
    )
    machine_details = map(parse_machine, machine_details)
    return machine_details


def process_machine(machine_details: tuple[int, int, int, int, int, int]) -> Optional[int]:
    ax, ay, bx, by, px, py = machine_details

    # Get target direction. Use Fraction to (1) get integer direction (i.e. lcm) and (2) avoid float
    # rounding errors
    p_grad = Fraction(py, px)  # Direction to get to target (i.e. gradient)
    assert Fraction(ay, ax) != Fraction(by, bx), 'Degenerate case--need to code for this :-('

    # Find k(=a_b_combo_ratio) such that (A + kB) is equal to `p_grad`
    a_b_combo_ratio = Fraction(ay - p_grad * ax, p_grad * bx - by)

    # For each step we take on this directional vector, how far do we travel (on x and y)?
    base_x_len = a_b_combo_ratio.denominator * ax + a_b_combo_ratio.numerator * bx
    base_y_len = a_b_combo_ratio.denominator * ay + a_b_combo_ratio.numerator * by

    # ...so how many of the base vectors do we need to get to target?
    num_of_base_vector = Fraction(px, base_x_len)

    # Check--must be the same if calculated on x or y axis
    num_of_base_vector_y = Fraction(py, base_y_len)
    assert num_of_base_vector == num_of_base_vector_y

    # If this is reachable, it must be an integer number of steps
    if num_of_base_vector.denominator != 1:
        # cannot get prize
        return None
    num_a = num_of_base_vector * a_b_combo_ratio.denominator
    num_b = num_of_base_vector * a_b_combo_ratio.numerator
    cost = num_a * 3 + num_b
    return int(cost)


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
