# Process time: 5.1 seconds.
import time
from collections import deque

def parse_input(line: str) -> tuple[deque[int], dict[int, tuple[int, int]]]:
    """
    Returns:
         disk_layout: deque of file_ids
         disk_files: dict where key=file_id and value=(file_length, free_space_length)
    """
    line = line + '0'  # last element has no free space
    disk_files = {}
    file_id = 0
    while line:
        file_len, space_len, *line = line
        disk_files[file_id] = (int(file_len), int(space_len))
        file_id += 1
    disk_layout = deque(disk_files)
    return disk_layout, disk_files


def compress(disk_layout: deque[int], disk_files: dict[int, tuple[int, int]]) -> list[int]:
    # iterate back through deque
    max_id = len(disk_layout)
    for this_id in reversed(range(max_id)):
        end_file_len, end_free_space = disk_files[this_id]
        for deque_pos in range(max_id):
            checking_id = disk_layout[deque_pos]
            if checking_id == this_id:
                # Any move now would be moving further from the current position
                break
            checking_file_len, checking_free_space = disk_files[checking_id]
            if end_file_len <= checking_free_space:
                # move file
                prior_file_id = disk_layout[disk_layout.index(this_id) - 1]
                disk_files[checking_id] = (checking_file_len, 0)
                if prior_file_id != checking_id:
                    # Move current file
                    disk_layout.remove(this_id)
                    disk_layout.insert(deque_pos + 1, this_id)
                    disk_files[checking_id] = (checking_file_len, 0)
                    disk_files[this_id] = (end_file_len, checking_free_space - end_file_len)
                    prior_len, prior_free_space = disk_files[prior_file_id]
                    disk_files[prior_file_id] = (prior_len, prior_free_space + end_file_len +
                                                 end_free_space)
                else:
                    # Just slide current file up along
                    disk_files[this_id] = (end_file_len, checking_free_space + end_free_space)
                break

    new_disk_layout = []
    for file_id in disk_layout:
        file_len, free_space = disk_files[file_id]
        new_disk_layout += ([file_id] * file_len + [0] * free_space)

    return new_disk_layout


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

    disk_layout, disk_files = parse_input(line)
    new_layout = compress(disk_layout, disk_files)
    answer = check_sum(new_layout)
    print(f'{answer=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
