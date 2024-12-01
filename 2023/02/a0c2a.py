import re

fname = r'02/input.txt'
# fname = r'02/test.txt'

# 12 red cubes, 13 green cubes, and 14 blue cubes
cols = dict(
    red=12,
    green=13,
    blue=14
)

sum = 0
with open(fname, 'r') as f:
    while ln:=f.readline():
        game = re.match('Game (\d+):', ln)
        if game is None:
            continue
        game = int(game.group(1))
        valid_pick = True
        for col in cols.keys():
            col_match = re.findall(f'(\d+) {col}', ln)
            max_this_col = max([int(this_match) for this_match in col_match] + [0])
            if cols[col] < max_this_col:
                valid_pick = False
        if valid_pick:
            sum += game
print(sum)
