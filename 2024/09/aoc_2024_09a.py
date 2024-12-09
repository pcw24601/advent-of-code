# Process time: 0.283 seconds.
import time
from collections import deque

def parse_input(line: str) -> deque[tuple[int,int,int]]:
    line = line + '0'  # last element has no free space
    disk_layout = deque()
    file_id = 0
    while line:
        file_len, space_len, *line = line
        disk_layout.append((file_id, int(file_len), int(space_len)))
        file_id += 1
    return disk_layout


def compress(disk_layout: deque[tuple[int,int,int]]) -> list[int]:
    start_id, start_file_len, free_space = disk_layout.popleft()
    new_layout = [start_id] * start_file_len
    end_id, end_file_len, _ = disk_layout.pop()
    while True:
        if not len(disk_layout):
            # might be some of last item to write
            new_layout += [end_id] * end_file_len
            break
        if not end_file_len:
            end_id, end_file_len, _ = disk_layout.pop()
        if free_space:
            move_length = min(free_space, end_file_len)
            new_layout += [end_id] * move_length
            end_file_len -= move_length
            free_space -= move_length
        else:
            start_id, start_file_len, free_space = disk_layout.popleft()
            new_layout += [start_id] * start_file_len
    return new_layout


def check_sum(new_layout: list[int]) -> int:
    check_sum = 0
    for pos, id in enumerate(new_layout):
        check_sum += pos * id
    return check_sum

def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        line = fp.read().strip()

    original_layout = parse_input(line)
    new_layout = compress(original_layout)
    answer = check_sum(new_layout)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
