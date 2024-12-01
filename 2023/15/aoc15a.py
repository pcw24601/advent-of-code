import re
from pprint import pprint

fname = r'15/input.txt'
# fname = r'15/test.txt'

with open(fname, 'r') as fp:
    input_seq = fp.read().strip()

input_list = input_seq.split(',')

total = 0
for ln in input_list:
    this_val = 0
    for char in ln:
        this_val += ord(char)
        this_val *= 17
        this_val %= 256
        # print(this_val)
    total += this_val

pprint(total)