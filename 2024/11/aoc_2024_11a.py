# Process time: 0.099 seconds.
import time


def process_number(orig_num: int) -> list[int]:
    if orig_num == 0:
        return [1]
    if not (orig_len:=len(orig_str:=str(orig_num))) % 2:
        # Even number of digits
        return [int(orig_str[:orig_len//2]), int(orig_str[orig_len//2:])]
    return [orig_num * 2024]


def process_list(orig_list: list[int]) -> list[int]:
    new_list = []
    for orig_num in orig_list:
        new_list += process_number(orig_num)
    return new_list

def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        line = fp.read().strip()

    stone_list = [int(x) for x in line.split()]
    for _ in range(25):
        stone_list = process_list(stone_list)

    print(f'{len(stone_list)=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
