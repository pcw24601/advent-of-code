from pprint import pprint
import numpy as np
from collections import namedtuple

fname = r'22/input.txt'
# fname = r'22/test.txt'

class Brick:
    def __init__(self, x1, y1, z1, x2, y2, z2, name):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2
        self.name = name + 1
    
    def __repr__(self):
        return f'Brick(x1={self.x1}, y1={self.y1}, z1={self.z1}, x2={self.x2}, y2={self.y2}, z2={self.z2})'
    
    def __lt__(self, other):
        return self.z1 < other.z1

    def add_to_grid(self, grid):
        # drop block down while slot on row below is empty
        while np.count_nonzero(grid[self.x1: self.x2+1, self.y1: self.y2+1, self.z1-1: self.z2]) == 0:
            self.z1 -= 1
            self.z2 -= 1
        grid[self.x1: self.x2+1, self.y1: self.y2+1, self.z1: self.z2+1] = self.name

    def rests_on_bricks(self, grid):
        """Return a list of brick numbers that this brick rests on"""
        bricks_set = set(np.unique(grid[self.x1: self.x2+1, self.y1: self.y2+1, self.z1-1]))
        bricks_set.discard(0)
        bricks_set.discard(-1)
        return bricks_set


with open(fname, 'r') as fp:
    lines = fp.readlines()

max_x = 0
max_y = 0
max_z = 0
bricks = []
for index_, ln in enumerate(lines):
    coords = ln.replace('~', ',').split(',')
    coords = (int(coord) for coord in coords)
    this_brick = Brick(*coords, index_)
    bricks.append(this_brick)
    max_x = max(max_x, this_brick.x1, this_brick.x2)
    max_y = max(max_y, this_brick.y1, this_brick.y2)
    max_z = max(max_z, this_brick.z1, this_brick.z2)

bricks.sort()
# pprint(bricks)

grid = np.zeros((max_x+1, max_y+1, max_z+1), int)
# set ground as -1
grid[:,:,0] = -1
key_bricks = set()  # set of bricks that are the only support for another brick
for brick in bricks:
    brick.add_to_grid(grid)
    if len(this_set:=brick.rests_on_bricks(grid)) == 1:
        key_bricks.update(this_set)
    # print(brick.name, brick.rests_on_bricks(grid))

# pprint(grid)
pprint(len(bricks) - len(key_bricks))
