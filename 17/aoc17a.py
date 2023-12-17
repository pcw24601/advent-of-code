import copy

fname = r'17/input.txt'
# fname = r'17/test.txt'

reverse_direction = dict(l='r', r='l', u='d', d='u')

class Tile():
    def __init__(self, line_num, col_num, heat_loss):
        self.line_num = line_num
        self.col_num = col_num
        self.heat_loss = heat_loss


class Route():
    def __init__(self, initial_heat_loss):
        self.path = ''
        self.line_num = 0
        self.col_num = 0
        self._heat_loss = -initial_heat_loss

    def move(self, direction):
        if direction == 'r':
            self.col_num += 1
        elif direction == 'l':
            self.col_num -= 1
        elif direction == 'u':
            self.line_num -= 1
        elif direction == 'd':
            self.line_num += 1
        else:
            print(f'Invalid direction: {direction}')
            raise ValueError
        self.path += direction
        return self
    

    @property
    def position(self):
        return self.line_num, self.col_num
    

    @property
    def recent_path(self):
        return self.path[-3:]
    

    @property
    def heat_loss(self):
        return self._heat_loss
    

    @heat_loss.setter
    def heat_loss(self, val):
        self._heat_loss = val


with open(fname, 'r') as fp:
    lines = fp.readlines()

print('Loading route')
tiles_dict = {}
for line_num, ln in enumerate(lines):
    for col_number, heat_loss in enumerate(ln.strip()):
        tiles_dict[(line_num, col_number)] = Tile(line_num, col_number, int(heat_loss))
last_line = line_num
last_col = col_number  

list_of_routes = [Route(tiles_dict[(0,0)].heat_loss)]
# total_heat_loss = set()
moves_dict = {}
print('Starting path search')
debug_loop_number = 0

while True:
    debug_loop_number += 1
    if not list_of_routes:
        print('All routes checked')
        break
    route = list_of_routes.pop(0)
    if not debug_loop_number % 1000:
        # print update info
        print(f'Loop: {debug_loop_number}, routes on list: {len(list_of_routes)}, heat_loss = {route.heat_loss}')

    # Check on a tile
    this_tile = tiles_dict.get(route.position, None)
    if this_tile is None:
        continue
    
    # Add heat_loss
    route.heat_loss += this_tile.heat_loss
    # Check if on end position
    if route.position == (last_line, last_col):
        total_heat_loss = route.heat_loss
        break
    # Add to moves set--check if we're on a loop AND have a higher heat loss
    route_loop_check = (route.position, route.recent_path)
    if route_loop_check in moves_dict:
        if moves_dict[route_loop_check] < route.heat_loss:
            continue
    moves_dict[route_loop_check] = route.heat_loss

    # Generate new positions
    possible_moves = set('rlud')
    recent_path = route.recent_path
    if recent_path:
        possible_moves.discard(reverse_direction[recent_path[-1]])  # cannot double back
    if len(recent_path) == 3:
        # check for going for three steps in a row
        if len(set(recent_path)) == 1:
            possible_moves.discard(recent_path[-1])
    for direction in possible_moves:
        list_of_routes.append(copy.deepcopy(route).move(direction))

    list_of_routes.sort(key=lambda route: route.heat_loss)

# if len(total_heat_loss) > 0:
#     # have found one route. If other routes are longer, discard
#     new_routes = [this_route for this_route in new_routes if this_route.heat_loss < min(total_heat_loss)]
# new_routes.sort(key=lambda route: route.heat_loss)
# list_of_routes = new_routes
# if not list_of_routes:
#     break

print(total_heat_loss)



