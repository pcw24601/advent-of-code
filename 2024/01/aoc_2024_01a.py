fname = 'input.txt'
l1 = []
l2 = []

with open(fname, 'r') as fp:
    lines = fp.readlines()

for line in lines:
    n1, n2 = line.strip('/n').split()
    l1.append(int(n1))
    l2.append(int(n2))

dist = 0
for n1, n2 in zip(sorted(l1), sorted(l2)):
    dist += abs(n1 - n2)

print(dist)
