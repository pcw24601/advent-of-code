import re

fname = 'input.txt'
# fname = 'test.txt'

with open(fname, 'r') as fp:
    instring = fp.read()

parsed = re.findall('mul\((\d+),(\d+)\)', instring)
result = sum(map(lambda tuple_: int(tuple_[0]) * int(tuple_[1]), parsed))
print(result)