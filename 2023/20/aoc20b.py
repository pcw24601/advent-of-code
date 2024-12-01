import math

# After inspection of graph.png

binstr = '1' * 12


#           CBA987654321
num1 = int('111101000011', 2)
num2 = int('111110010101', 2)
num3 = int('111101011011', 2)
num4 = int('111101111111', 2)

print(math.lcm(num1, num2, num3, num4))