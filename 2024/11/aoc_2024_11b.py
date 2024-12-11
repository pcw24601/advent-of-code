# Process time: 0.0749 seconds.
import time
from collections import Counter


def process_number(orig_num: int) -> list[int]:
    if orig_num == 0:
        return [1]
    if not (orig_len:=len(orig_str:=str(orig_num))) % 2:
        # Even number of digits
        return [int(orig_str[:orig_len//2]), int(orig_str[orig_len//2:])]
    return [orig_num * 2024]


def process_list(orig_list: list[int]) -> Counter:
    stones = Counter(orig_list)
    new_stones = Counter()
    for stone_id, count in stones.items():
        this_stone_new_stones = process_number(stone_id)
        for this_new_stone in this_stone_new_stones:
            new_stones[this_new_stone] += count
    return new_stones


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        line = fp.read().strip()

    stone_list = [int(x) for x in line.split()]
    for i in range(75):
        stone_list = process_list(stone_list)

    answer = sum(stone_list.values())
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
