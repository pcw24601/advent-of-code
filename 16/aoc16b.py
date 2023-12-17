import copy

fname = r'16/input.txt'
# fname = r'16/test.txt'

class Beam():
    def __init__(self, dir, row, col):
        self.dir = dir
        self.col = col
        self.row = row

    def move(self, direction):
        if direction == 'r':
            self.col += 1
        elif direction == 'l':
            self.col -= 1
        elif direction == 'u':
            self.row -= 1
        elif direction == 'd':
            self.row += 1
        else:
            print(f'Invalid direction: {direction}')
            raise ValueError
        return self
    
    @property
    def position(self):
        return self.row, self.col
       


class Tile():
    def __init__(self, symbol, line_num, col_num):  # pos = (line_num, row_num)
        self.symbol = symbol
        self.energised = False
        self.line = line_num
        self.col = col_number
        self.gone = {direction: False for direction in 'lrud'}
    
    def move_through_dir(self, direction):
        if self.gone[direction]:
            # Entering loop
            return []
        self.gone[direction] = True
        self.energised = True
        symb = self.symbol
        if symb == '.':
            return [Beam(direction, self.line, self.col).move(direction)]
        
        elif symb == '-':
            if direction in ['u', 'd']:
                return[Beam('r', self.line, self.col).move('r'),
                       Beam('l', self.line, self.col).move('l')]
            else:
                return [Beam(direction, self.line, self.col).move(direction)]
            
        elif symb == '|':
            if direction in ['l', 'r']:
                return[Beam('u', self.line, self.col).move('u'),
                       Beam('d', self.line, self.col).move('d')]
            else:
                return [Beam(direction, self.line, self.col).move(direction)]
            
        elif symb == '/':
            if direction == 'r':
                new_direction = 'u'
            elif direction == 'l':
                new_direction = 'd'
            elif direction == 'u':
                new_direction = 'r'
            elif direction == 'd':
                new_direction = 'l'
            return [Beam(new_direction, self.line, self.col).move(new_direction)]
        
        elif symb == '\\':
            if direction == 'r':
                new_direction = 'd'
            elif direction == 'l':
                new_direction = 'u'
            elif direction == 'u':
                new_direction = 'l'
            elif direction == 'd':
                new_direction = 'r'
            return [Beam(new_direction, self.line, self.col).move(new_direction)]

        else:
            print(f'Invalid tile symbol: "{symb}"')
            raise ValueError



with open(fname, 'r') as fp:
    lines = fp.readlines()

orig_tiles_dict = {}
for line_num, ln in enumerate(lines):
    for col_number, tile_symbol in enumerate(ln.strip()):
        orig_tiles_dict[(line_num, col_number)] = Tile(tile_symbol, line_num, col_number)

max_line_num = line_num  # Check no blank lines at end
max_col_number = col_number


def get_energised_count(direction, entry_line, entry_col):
    beam_list = [Beam(direction, entry_line, entry_col)]

    while True:
        new_beam_list = []
        for beam in beam_list:
            pos = beam.position
            if pos in tiles_dict:
                new_beam_list += tiles_dict[pos].move_through_dir(beam.dir)
        if new_beam_list == []:
            break
        beam_list = new_beam_list

    # get total sum
    total_energised = 0
    for tile in tiles_dict.values():
        if tile.energised:
            total_energised += 1
    
    return total_energised


# print(get_energised_count('d', 0, 3))
max_energised = 0

for entry_line in range(max_line_num + 1):
    for entry_col, direction in [(0, 'r'), (max_col_number, 'l')]:
        tiles_dict = copy.deepcopy(orig_tiles_dict)
        total_energised = get_energised_count(direction, entry_line, entry_col)
 
        max_energised = max(max_energised, total_energised)

for entry_col in range(max_col_number + 1):
    for entry_line, direction in [(0, 'd'), (max_line_num, 'u')]:
        tiles_dict = copy.deepcopy(orig_tiles_dict)
        total_energised = get_energised_count(direction, entry_line, entry_col)
 
        max_energised = max(max_energised, total_energised)

print(max_energised)
