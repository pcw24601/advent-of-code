import re

fname = 'input.txt'
# fname = 'test_b.txt'

with open(fname, 'r') as fp:
    in_string = fp.read()
# new lines will mess with regex parsing
in_string = in_string.replace('\n', 'X')
# Possible edge case--replace chunk with 'X' in case part before and after removed section forms
# a new mul command

# Lazily strip everything between `don't()` and `do()`
enabled_string = re.sub(r"don\'t\(\).*?do\(\)", "X", in_string)
# If there's any remaining `don't()`, remove everything after it
enabled_string = re.sub(r"don\'t\(\).*", "", enabled_string)

parsed = re.findall('mul\((\d+),(\d+)\)', enabled_string)
result = sum(map(lambda tuple_: int(tuple_[0]) * int(tuple_[1]), parsed))
print(result)
