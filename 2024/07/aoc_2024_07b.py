# Process time: 9.99 seconds.
import itertools
import operator
from time import time

def concat_numbers(a: int, b: int) -> int:
    return int(str(a) + str(b))


def check_line(line: list[int]) -> int:
    target, start_number, *other_numbers = line
    num_ops = len(other_numbers)
    operator_list = [operator.add, operator.mul, concat_numbers]
    for operator_sequence in itertools.product(operator_list, repeat=num_ops):
        this_total = start_number
        for this_op, next_number in zip(operator_sequence, other_numbers):
            this_total = this_op(this_total, next_number)
        if this_total == target:
            return this_total
    return 0


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