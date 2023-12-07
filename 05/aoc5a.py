import re

fname = r'05/input.txt'
fname = r'05/test.txt'

list_of_maps = []

with open(fname, 'r') as f:
    # read seeds
    ln = f.readline()
    seeds = [int(seed_str) for seed_str in re.findall(r'\d+', ln)]

    this_map = []
    #loop through maps
    while ln:=f.readline():
        if re.search('map:', ln) is not None:
            if this_map:
                list_of_maps.append(this_map)
            this_map = []
            continue
        map_coords = re.findall(r'\d+', ln) # dest, source, range
        if len(map_coords) == 3:
            map_coords = [int(coord) for coord in map_coords]
            this_map.append(
                dict(
                    dest=map_coords[0],
                    source=map_coords[1],
                    length=map_coords[2]
                )
            )

list_of_maps.append(this_map)

seed_dict = {}
for seed in seeds:
    op = seed
    for this_map in list_of_maps:
        for map_element in this_map:
            if map_element['source'] <= op < (map_element['source'] + map_element['length']):
                op = op - map_element['source'] + map_element['dest']
                break


    seed_dict[seed] = op


print(min(list(seed_dict.values())))
