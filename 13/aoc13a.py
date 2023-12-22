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

def get_horz_score(pattern):
    horz_match_score = 0
    num_lines = len(pattern)
    for line_num in range(num_lines - 1):
        if pattern[line_num] == pattern[line_num+1]:
            match_score = line_num + 1
            for l1, l2 in zip(range(line_num-1,-1,-1), range(line_num+2,num_lines)):
                if pattern[l1] != pattern[l2]:
                    match_score = 0
                    break
            horz_match_score += match_score
    
    return horz_match_score



for pattern in pattern_list:
    horz_match_score += get_horz_score(pattern)
    vert_match_score += get_horz_score(transpose(pattern))


print(f'{horz_match_score=}, {vert_match_score=}, total = {100 * horz_match_score + vert_match_score}')

