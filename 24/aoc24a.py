import numpy as np
from pprint import pprint

fname = r'24/input.txt'
# fname = r'24/test.txt'

with open(fname, 'r') as fp:
    lines = fp.readlines()

XMIN = YMIN = 200000000000000
XMAX = YMAX = 400000000000000
# XMIN = YMIN = 7
# XMAX = YMAX = 27

class Hailstone():
    def __init__(self, x, y, z, vx, vy, vz):
        self.x0 = int(x)
        self.y0 = int(y)
        self.z0 = int(z)
        self.vx = int(vx)
        self.vy = int(vy)
        self.vz = int(vz)


    def __repr__(self):
        return f'Hailstone: position ({self.x0}, {self.y0}, {self.z0}), velocity ({self.vx}, {self.vy}, {self.vz})'
    

    def get_t(self, *, x=None, y=None):
        """Get t from either x or y"""
        if x is not None:
            t = (x - self.x0) / self.vx
        else:
            t = (y - self.y0) / self.vy
        return t
    
    @property
    def a(self):
        return np.array([[self.vx, -self.vy]], np.float_, ndmin=2)
    
    @property
    def b(self):
        return np.array([self.vx * self.y0 - self.vy * self.x0], np.float_, ndmin=1)
    

    def collision_position(self, other):
        """Return x, y position of collision"""
        a_mat = np.concatenate([self.a, other.a])
        b_mat = np.concatenate([self.b, other.b])
        result = np.dot(np.linalg.inv(a_mat), b_mat)
        return result
    
    def test_collision(self, other):
        # print(f'{self}, {other}')
        try:
            result = self.collision_position(other)
            print(result)
        except np.linalg.LinAlgError as e:
            # Singluar matrix: no solution, parallel lines
            # print(" no match")
            return False
        if (result < XMIN).any():
            # print(' too low')
            return False
        if (result > XMAX).any():
            # print(' too high')
            return False
        if self.get_t(y=result[0]) < 0:
            # print(' self in the past')
            return False
        if other.get_t(y=result[0]) < 0:
            # print(' other in the past')
            return False
        
        # print(' added')
        return True
    



hail_list = []
for ln in lines:
    pos_vel = ln.strip().replace('@', ',').split(r',')
    hail_list.append(Hailstone(*pos_vel))

# pprint(hail_list)
# pprint(np)

# pprint(hail_list[0].collision_position(hail_list[1]))

track_collisions = 0
for index_1 in range(len(hail_list) - 1):
    for index_2 in range(index_1 + 1, len(hail_list)):
        track_collisions += hail_list[index_1].test_collision(hail_list[index_2])

print(track_collisions)
