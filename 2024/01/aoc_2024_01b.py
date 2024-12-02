# Post solution note: could actually be done quite nicely with two counters, one for each list,
# and the result being a sum of n1 * n1_freq * n2_freq
from collections import Counter

fname = 'input.txt'
l1 = []
l2 = []

with open(fname, 'r') as fp:
    lines = fp.readlines()

for line in lines:
    n1, n2 = line.strip('/n').split()
    l1.append(int(n1))
    l2.append(int(n2))

l2_freq = Counter(l2)

sim_score = 0
for n1 in l1:
    sim_score += n1 * l2_freq[n1]
print(sim_score)
