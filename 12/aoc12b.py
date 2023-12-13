import re
from pprint import pprint

fname = r'12/input.txt'
# fname = r'12/test.txt'

with open(fname, 'r') as fp:
    input_list = fp.readlines()

puzzle_def = []
for ln in input_list:
    line, lengths = ln.split()
    # Unfold input
    line = line + f'?{line}'*4
    line += '.'  # add '.' to end to help regex later
    lengths = lengths + f',{lengths}'*4
    lengths = lengths.split(',')
    lengths = [int(length) for length in lengths]
    this_dict = dict(line=line, lengths=lengths)
    puzzle_def.append(this_dict)
    # print(line.split('?', maxsplit=1))


def recursive_count_matches(sub_string, lengths):
    sub_string = sub_string.lstrip('.')
    if len(lengths) == 0:
        if '#' in sub_string:
            # nothing more in lengths but still a spring
            return 0
        else:
            # nothing more in lengths and remaining string has no more '#'
            return 1

    if len(sub_string) == 0:
        # No more strings but still something in lengths list
        return 0
    
    # Terminate early if insufficient '#' to fit
    num_hashes = sub_string.count('#')
    num_qs = sub_string.count('?')
    num_springs = sum(lengths)
    groups_needed = len(lengths)

    if sum(lengths) > (num_hashes + num_qs):
        # If every '?' became a '#' there wouldn't be enough
        return 0
    
    existing_number_groups = len(sub_string.replace('.', ' ').split())
    if num_springs > (num_hashes + num_qs + existing_number_groups - groups_needed):
        return 0

    
    first_char = sub_string[0]
    if first_char == '#':
        regex_obj = re.compile('[#?]{' + str(lengths[0]) + '}[^#](.*$)')
        these_matches = re.match(regex_obj, sub_string)
        if these_matches is None:
            # Can't match lenght of '#' or '?' not followed by a '#'
            return 0
        else:
            # Strip and try to match on rest of string
            # print(f'line = {these_matches.group(0)}, next = {these_matches.group(1)}')
            return recursive_count_matches(these_matches.group(1), lengths[1:])
        
    # first character must be '?'
    dot_count = recursive_count_matches('.' + sub_string[1:], lengths)
    hash_count = recursive_count_matches('#' + sub_string[1:], lengths)
    return dot_count + hash_count


total = 0
for i, line_dict in enumerate(puzzle_def):
    print(f'Checking line {i+1}, {line_dict["line"]}')
    this_sum = recursive_count_matches(line_dict['line'], line_dict['lengths'])
    print(this_sum)
    total += this_sum

print(total)