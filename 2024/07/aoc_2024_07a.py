import itertools
import operator

fname = 'input.txt'
# fname='test.txt'

with open(fname, 'r') as fp:
    lines = fp.read().splitlines()

parsed_lines = []
for line in lines:
    target, numbers = line.split(':')
    parsed_lines.append([int(target)] + list(map(int, numbers.split())))

def check_line(line: list[int]) -> int:
    target, start_number, *other_numbers = line
    # We need an operator ('+' or '*') before each element of other_numbers. Loop through all
    # possible permutations of these operators, with an early return if we get the target.
    num_ops = len(other_numbers)
    for operator_sequence in itertools.product([operator.add, operator.mul], repeat=num_ops):
        this_total = start_number
        for this_op, next_number in zip(operator_sequence, other_numbers):
            this_total = this_op(this_total, next_number)
        if this_total == target:
            return this_total
    return 0


answer = sum(map(check_line, parsed_lines))
print(f'{answer=}')
