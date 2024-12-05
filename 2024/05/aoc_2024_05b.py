import re
from collections import defaultdict

fname = 'input.txt'
# fname='test.txt'

with open(fname, 'r') as fp:
    lines = fp.read()
rules_str, print_order_str = lines.split('\n\n')

# parse rules
# `rules_dict` is a default dict, where each key is the first page number, and the value is a set
# of page numbers that cannot come after the key
rules_dict = defaultdict(set)
rules = re.findall(r'(\d+)\|(\d+)', rules_str)
for rule in rules:
    rules_dict[int(rule[0])].add(int(rule[1]))

# parse print order list
# `print_order_list` is a list of lists of the page numbers to be printed
print_order_list = []
for line in print_order_str.split('\n'):
    print_order = re.findall(r'\d+', line)
    print_order_list.append([int(page_num) for page_num in print_order])


def fix_print_list(print_order):
    # For each page in a print order, check if the prior pages are allowed to be printed before
    # it. If not, return 0, else return the value of the middle page in the print_order
    if not print_order:
        return 0
    for item_num, page in enumerate(print_order):
        if rules_dict[page] & set(print_order[:item_num]):
            correct_order = sort_print_list(print_order)
            return correct_order[len(print_order) // 2]
    return 0


def sort_print_list(print_order: list):
    finished = False
    while not finished:
        finished = True
        # ?ripple sort
        for item_num, page in enumerate(print_order):
            if rules_dict[page] & set(print_order[:item_num]):
                print_order[item_num], print_order[item_num-1] \
                    = (print_order[item_num -1 ], print_order[item_num])
                finished = False
    return print_order


answer = sum(map(fix_print_list, print_order_list))
print(f'{answer=}')
