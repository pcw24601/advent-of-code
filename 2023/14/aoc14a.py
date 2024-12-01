import re
from pprint import pprint

fname = r'14/input.txt'
# fname = r'14/test.txt'


def transpose(input_list):
    dim_1 = len(input_list)
    dim_2 = len(input_list[0])  # assume all same length

    output_list = []
    for x in range(dim_2):
        output_list.append("")
        for y in range(dim_1):
            output_list[x] += input_list[y][x]
    return output_list
# TEST:
# pprint(transpose(["abcd", "efgh"]))


def count_os(input_str, first_row_num):
    this_str, *other_str = input_str.split('#', maxsplit=1)

    # count 'O' in this_str
    count = this_str.count('O')
    # first term below corrects for the starting position not being 0, second term is sum of all integers up to 'count'
    score = (count * first_row_num) + (count * (count + 1))/2  # first_row_number is zero-indexed row number

    
    # if other_str not empty, recurse on other_string
    if len(other_str) > 0:
        next_count, next_score = count_os(other_str[0], first_row_num + len(this_str) + 1)
        count += next_count
        score += next_score

    # return (num_rocks, running_score)
    return count, score


input_list = []
with open(fname, 'r') as fp:
    while ln:=fp.readline():
        input_list.append(ln.strip())
# pprint(input_list)

input_list = transpose(input_list)
# pprint(input_list)

score = 0
for ln in input_list:
    this_count, this_score = count_os(ln, 0)
    # print(f'{this_score=}')
    # Correct to count from south edge, not north
    this_score = (this_count) * (len(input_list)+1) - this_score
    score += this_score
# print(count_os(input_list[], 0))

print(int(score))
