import re

fname = r'04/input.txt'
# fname = r'04/test.txt'

sum = 0

with open(fname, 'r') as f:
    while ln:=f.readline():
        my_nums = re.findall(r': .* \| ', ln)
        winning_nums = re.findall(r'\| .*', ln)

        my_nums = re.findall(r'\d+', my_nums[0])
        winning_nums = re.findall(r'\d+', winning_nums[0])

        num_winning_nums = len(set(my_nums).intersection(set(winning_nums)))
        if num_winning_nums > 0:
            sum += 2 ** (num_winning_nums - 1)

        # print(f'{my_nums=}  |  {winning_nums=} | {set(my_nums).intersection(set(winning_nums))} | {sum=}')


print(sum)