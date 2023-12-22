from pprint import pprint

fname = r'13/input.txt'
# fname = r'13/test.txt'

def transpose(input_list):
    dim_1 = len(input_list)
    dim_2 = len(input_list[0])  # assume all same length

    output_list = []
    for x in range(dim_2):
        output_list.append("")
        for y in range(dim_1):
            output_list[x] += input_list[y][x]
    return output_list

# Load input
with open(fname, 'r') as fp:
    lines = fp.readlines()

pattern_list = []
this_pattern = []
for ln in lines:
    ln = ln.strip()
    if not ln:
        pattern_list.append(this_pattern)
        this_pattern = []
    else:
        this_pattern.append(ln)
pattern_list.append(this_pattern)  # need to add last pattern

# pprint(pattern_list)

horz_match_score = vert_match_score = 0

def get_horz_score(pattern, acceptable_num_differences, invalid_line=None):
    # Put mirror in each location and get locations with only one difference between reflection and original
    num_lines = len(pattern)
    for line_num in range(num_lines - 1):
        differences = 0
        for l1, l2 in zip(range(line_num,-1,-1), range(line_num+1,num_lines)):
            differences += sum([c1 != c2 for c1, c2 in zip(pattern[l1], pattern[l2])])
        if differences == acceptable_num_differences:
            if line_num + 1 != invalid_line:  # check--is this the original reflection?
                return line_num + 1       

    return 0  # no match found


for pattern in pattern_list:
    horz_match_score += get_horz_score(pattern, 1, get_horz_score(pattern, 0))
    pattern = transpose(pattern)
    vert_match_score += get_horz_score(pattern, 1, get_horz_score(pattern, 0))


print(f'{horz_match_score=}, {vert_match_score=}, total = {100 * horz_match_score + vert_match_score}')

