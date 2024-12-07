# Original process time: 9.99 seconds.
# This recursive version: 1.63 seconds
import itertools
import operator
from time import time

def concat_numbers(a: int, b: int) -> int:
    return int(str(a) + str(b))

def check_sub_line(target, current_total, other_numbers):
    if current_total > target:
        # early return, operations can only increase total
        return 0
    if not other_numbers:
        return target if current_total == target else 0
    for this_operator in (operator.add, operator.mul, concat_numbers):
        new_total = this_operator(current_total, other_numbers[0])
        if this_calibration:=check_sub_line(target, new_total, other_numbers[1:]):
            return this_calibration
    return 0

def check_line(line: list[int]) -> int:
    target, start_number, *other_numbers = line
    return check_sub_line(target, start_number, tuple(other_numbers))


def main():
    fname = 'input.txt'
    # fname='test.txt'

    with open(fname, 'r') as fp:
        lines = fp.read().splitlines()

    parsed_lines = []
    for line in lines:
        target, numbers = line.split(':')
        parsed_lines.append([int(target)] + list(map(int, numbers.split())))

    answer = sum(map(check_line, parsed_lines))
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time()
    main()
    print(f"Process time: {round(time() - start_time, 2)} seconds.")