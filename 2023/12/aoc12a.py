import re
from pprint import pprint

fname = r'12/input.txt'
fname = r'12/test.txt'

with open(fname, 'r') as fp:
    input_list = fp.readlines()

puzzle_def = []
for ln in input_list:
    line, lengths = ln.split()
    lengths = lengths.split(',')
    lengths = [int(length) for length in lengths]
    this_dict = dict(line=line, lengths=lengths)
    puzzle_def.append(this_dict)
    # print(line.split('?', maxsplit=1))

# pprint(puzzle_def)
# Output:
# [{'lengths': ['1', '1', '3'], 'line': '???.###'},
#  {'lengths': ['1', '1', '3'], 'line': '.??..??...?##.'},
#  {'lengths': ['1', '3', '1', '6'], 'line': '?#?#?#?#?#?#?#?'},
#  {'lengths': ['4', '1', '1'], 'line': '????.#...#...'},
#  {'lengths': ['1', '6', '5'], 'line': '????.######..#####.'},
#  {'lengths': ['3', '2', '1'], 'line': '?###????????'}]

def count_string_matches(string_, lengths):
    """Takes a string and a list of lengths. If the string can be made consistent with the lengths, returns 1, otherwise returns 0."""
    pre_str, *post_str = string_.split('?', maxsplit=1)  # removes first '?' and splits string
    end_of_string = False
    if post_str == []:  # No '?' in string ('?' at the end gives [''])
        end_of_string = True
    else:
        post_str = post_str[0]
    spring_groups = re.findall(r'#+', pre_str)

    # check substring matches:
    short_group = False
    i = 0  # Need in case there are no springs in the test line
    for i, spring_group in enumerate(spring_groups):
        if short_group:
            # Last group was too short and not at end of pre_str
            return 0
        try:
            this_len = lengths[i]
        except IndexError:
            # There are more spring groups than indicies in 'lengths'
            return 0
        if len(spring_group) > this_len:
            return 0  # doesn't match
        if len(spring_group) < this_len:
            short_group = True

    if not end_of_string:
        return count_string_matches(pre_str + '.' + post_str, lengths) + count_string_matches(pre_str + '#' + post_str, lengths)
    elif (not short_group) and (len(lengths) == i+1):  # check we've matched all lengths
        return 1
    else: # not all matched
        return 0

total = 0
for i, line_dict in enumerate(puzzle_def):
    print(f'Checking line {i+1}, {line_dict["line"]}')
    this_sum = count_string_matches(line_dict['line'], line_dict['lengths'])
    print(this_sum)
    total += this_sum

print(total)