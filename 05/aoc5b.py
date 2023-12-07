import re
from pprint import pprint

fname = r'05/input.txt'
# fname = r'05/test.txt'

list_of_maps = []

with open(fname, 'r') as f:
    # read seeds
    ln = f.readline()
    seeds = [dict(start=int(seed_str[0]), length=int(seed_str[1]))
             for seed_str in re.findall(r'(\d+) (\d+)', ln)
            ]  # seeds = [{start: 79, length: 14}, ...]
    # print(seeds)
             

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

ip_dict_list = seeds

for this_map in list_of_maps:
    re_run = True
    while re_run:
        ip_dict_list_split = []
        re_run = False
        for ip_dict in ip_dict_list:
            copy_ip_dict = True
            ip_s = ip_dict['start']
            ip_e = ip_s + ip_dict['length']
            for map_dict in this_map:
                mp_s = map_dict['source']
                mp_e = mp_s + map_dict['length']
                if ip_s < mp_e < ip_e:
                    ip_dict_list_split.append(dict(start=ip_s,
                                            length=mp_e-ip_s
                                            ))
                    ip_dict_list_split.append(dict(start=mp_e,
                                            length=ip_e-mp_e))
                    re_run = True
                    copy_ip_dict = False
                    break
                elif ip_s < mp_s < ip_e:
                    ip_dict_list_split.append(dict(start=ip_s,
                                            length=mp_s-ip_s))
                    ip_dict_list_split.append(dict(start=mp_s,
                                            length=ip_e-mp_s))
                    re_run = True
                    copy_ip_dict = False
                    break
            if copy_ip_dict:
                ip_dict_list_split.append(ip_dict)
        ip_dict_list = ip_dict_list_split
    
    # Now we have op_dict_list where no ranges are split across maps
    ip_dict_list = []
 
    for ip_dict in ip_dict_list_split:
        op_dict = ip_dict.copy()
        for map_element in this_map:
            if map_element['source'] <= ip_dict['start'] < (map_element['source'] + map_element['length']):
                op_dict['start'] = ip_dict['start'] - map_element['source'] + map_element['dest']
                break
        ip_dict_list.append(op_dict)

print(min([ip_dict['start'] for ip_dict in ip_dict_list]))
