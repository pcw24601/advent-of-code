# Process time: 0.000989 seconds.
import math
import time
import re
from collections import Counter
from typing import Optional


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


def main():
    fname = 'input.txt'; max_x, max_y, num_seconds = 101, 103, 100
    # fname = 'test.txt'; max_x, max_y, num_seconds = 11, 7, 100

    with open(fname, 'r') as fp:
        line = fp.read()

    pv_list = re.findall(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)', line)
    pv_list = [tuple(map(int, pv)) for pv in pv_list]
    new_positions = map(lambda pv: new_pv(pv, max_x, max_y, num_seconds), pv_list)
    quadrants = map(lambda pv: find_quadrant(pv, max_x, max_y), new_positions)
    quadrant_counter = Counter(quadrants)
    del quadrant_counter[None]

    answer = math.prod(quadrant_counter.values())

    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
