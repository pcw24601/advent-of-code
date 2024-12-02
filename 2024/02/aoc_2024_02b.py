import pandas as pd

fname = 'input.txt'
# fname = 'test.txt'
l1 = []
l2 = []

with open(fname, 'r') as fp:
    lines = fp.readlines()

def safe(line:str):
    vals = pd.Series(line.strip().split()).astype(int)
    for drop_level in vals.index:
        damped_vals = vals.drop(drop_level)
        diff = damped_vals.diff().dropna()
        if -3 <= diff.min() <= diff.max() <= -1:
            return True
        if 1 <= diff.min() <= diff.max() <= 3:
            return True
    return False

print(sum(map(safe, lines)))
