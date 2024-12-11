# Process time: 0.0762 seconds.
# Alternative method--default lur_cache size (128) is too small, works with @cache
import time
from functools import cache


# @lru_cache
def process_number(orig_num: int) -> list[int]:
    if orig_num == 0:
        return [1]
    if not (orig_len:=len(orig_str:=str(orig_num))) % 2:
        # Even number of digits
        return [int(orig_str[:orig_len//2]), int(orig_str[orig_len//2:])]
    return [orig_num * 2024]


@cache
def process_number_n_times(orig_num: int, num_reps: int) -> int:
    next_num_list = process_number(orig_num)
    num_reps -= 1
    if num_reps > 0:
        num_stones = sum([process_number_n_times(this_num, num_reps) for this_num in next_num_list])
        return num_stones
    return len(next_num_list)


def process_list(orig_list: list[int], num_blinks: int) -> int:
    num_stones = 0
    for orig_num in orig_list:
        num_stones += process_number_n_times(orig_num, num_blinks)
    return num_stones


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        line = fp.read().strip()

    stone_list = [int(x) for x in line.split()]
    num_stones = process_list(stone_list, 75)

    print(f'{num_stones=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
