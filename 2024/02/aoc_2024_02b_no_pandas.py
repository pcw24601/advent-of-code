fname = 'input.txt'
# fname = 'test.txt'
l1 = []
l2 = []

with open(fname, 'r') as fp:
    lines = fp.readlines()

def calc_diff(l: list) -> list:
    return list(map(lambda x, y: x - y, l[1:], l[:-1]))

def safe(line:str):
    vals = list(map(int, line.strip().split()))
    for drop_level in range(len(vals)):
        damped_levels = vals[:drop_level] + vals[drop_level+1:]
        diff = calc_diff(damped_levels)
        if -3 <= min(diff) <= max(diff) <= -1:
            return True
        if 1 <= min(diff) <= max(diff) <= 3:
            return True
    return False

print(sum(map(safe, lines)))
