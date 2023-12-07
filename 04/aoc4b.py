import re

fname = r'04/input.txt'
# fname = r'04/test.txt'

matches_dict = {}

with open(fname, 'r') as f:
    while ln:=f.readline():
        my_nums = re.findall(r': .* \| ', ln)
        winning_nums = re.findall(r'\| .*', ln)
        card_num = re.match('Card *(\d+)', ln)
        if card_num is None:
            break
        card_num = int(card_num.group(1))

        my_nums = re.findall(r'\d+', my_nums[0])
        winning_nums = re.findall(r'\d+', winning_nums[0])

        num_winning_nums = len(set(my_nums).intersection(set(winning_nums)))
        matches_dict[card_num] = num_winning_nums

        # print(f'{my_nums=}  |  {winning_nums=} | {set(my_nums).intersection(set(winning_nums))}')

# print(matches_dict) 

num_cards = {key: 1 for key in matches_dict}
sum = 0

for key in sorted(matches_dict.keys()):
    for new_key in range(key+1, key+matches_dict[key]+1):
        if new_key in matches_dict:
            num_cards[new_key] += num_cards[key]
    sum += num_cards[key]

print(sum) 
