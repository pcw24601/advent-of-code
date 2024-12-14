# (with some help on heuristics from Reddit)
import math
import time
import re
from collections import Counter, defaultdict
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np


def new_pv(
        pv: tuple[int, int, int, int],
        max_x: int,
        max_y: int,
        num_seconds,
) -> tuple[int, int, int, int]:
    px, py, vx, vy = pv
    px = (px + vx * num_seconds) % max_x
    py = (py + vy * num_seconds) % max_y

    return px, py, vx, vy


def find_quadrant(
        pv: tuple[int, int, int, int],
        max_x: int,
        max_y: int,
) -> Optional[int]:
    px, py, vx, vy = pv
    if px == max_x // 2 or py == max_y // 2:
        return None
    quadrant = 0
    if px > max_x // 2:
        quadrant += 1
    if py > max_y // 2:
        quadrant += 2
    return quadrant


def find_danger_level(pv_list, max_x, max_y):
    quadrants = map(lambda pv: find_quadrant(pv, max_x, max_y), pv_list)
    quadrant_counter = Counter(quadrants)
    del quadrant_counter[None]

    return math.prod(quadrant_counter.values())


def display(pv_list, max_x, max_y):
    display = []
    for _ in range(max_y):
        display.append([' '] * max_x)

    for px, py, _, _ in pv_list:
        display[py][px] = '*'

    for row_num, row in enumerate(display):
        for val in row:
            print(val, end='')
        print('     ', end='')

        print()
        time.sleep(0.005)


def create_image(pv_list, max_x, max_y):
    image = np.zeros((max_x, max_y))
    for px, py, _, _ in pv_list:
        image[px, py] = 255
    return image


def main():
    fname = 'input.txt'; max_x, max_y = 101, 103
    # fname = 'test.txt'; max_x, max_y = 11, 7

    with open(fname, 'r') as fp:
        line = fp.read()

    pv_list = re.findall(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
    pv_list = [tuple(map(int, pv)) for pv in pv_list]
    # danger_level = find_danger_level(pv_list, max_x, max_y)
    danger_levels = {}
    for num_seconds in range(10000):
        new_positions = map(lambda pv: new_pv(pv, max_x, max_y, num_seconds), pv_list)
        this_danger_level = find_danger_level(new_positions, max_x, max_y)
        danger_levels[num_seconds] = this_danger_level

    # sort by danger level
    print('sorting')
    sorted_danger_levels = {k: v for k, v in sorted(danger_levels.items(), key=lambda x: x[1])}

    for num_vals, sec in enumerate(sorted_danger_levels):
        if num_vals > 500:
            break
        # image = create_image(sorted_danger_levels[sec], max_x, max_y)
        new_positions = map(lambda pv: new_pv(pv, max_x, max_y, sec), pv_list)
        image = create_image(new_positions, max_x, max_y)
        plt.imsave(f'figs_sorted/{num_vals}_{sec}_im.png', image)


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
