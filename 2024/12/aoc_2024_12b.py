# Process time: 0.0356 seconds.
import time
from itertools import product


def find_perim_area(
        row, col, grid, unprocessed_points, num_rows, num_cols
) -> tuple[int, set, set, set, set]:
    area = 1
    u_edges = set()
    l_edges = set()
    d_edges = set()
    r_edges = set()
    for direction, row_diff, col_diff in [
        ('u', -1, 0),
        ('d', 1, 0),
        ('l', 0, -1),
        ('r', 0, 1)
    ]:
        current_plant = grid[row][col]
        new_row = row + row_diff
        new_col = col + col_diff
        if (0 <= new_row < num_rows) and (0 <= new_col < num_cols):
            # Not edge
            new_plant = grid[new_row][new_col]
            if new_plant == current_plant:
                # Same plot
                if (new_row, new_col) in unprocessed_points:
                    unprocessed_points.remove((new_row, new_col))
                    this_area, this_u_edges, this_l_edges, this_d_edges, this_r_edges \
                        = find_perim_area(new_row, new_col, grid, unprocessed_points, num_rows,
                                          num_cols)
                    area += this_area
                    u_edges |= this_u_edges
                    l_edges |= this_l_edges
                    d_edges |= this_d_edges
                    r_edges |= this_r_edges
                continue
        # Border with edge or different plot
        match direction:
            case 'u':
                u_edges.add((row, col))
            case 'd':
                d_edges.add((row, col))
            case 'l':
                l_edges.add((row, col))
            case 'r':
                r_edges.add((row, col))
    return area, u_edges, l_edges, d_edges, r_edges


def remove_linked_edges(edges: set[tuple[int, int]], row_inc: int, col_inc: int):
    this_row, this_col = edges.pop()
    for direction in {1, -1}:
        new_row = this_row + direction * row_inc
        new_col = this_col + direction * col_inc
        try:
            while True:
                edges.remove((new_row, new_col))
                new_row += direction * row_inc
                new_col += direction * col_inc
        except KeyError:
            pass


def find_num_edges(edges: set[tuple[int, int]], row_inc: int, col_inc: int) -> int:
    num_edges = 0
    while len(edges):
        num_edges += 1
        remove_linked_edges(edges, row_inc, col_inc)
    return num_edges


def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    with open(fname, 'r') as fp:
        grid = fp.read().splitlines()

    num_rows = len(grid)
    num_cols = len(grid[0])
    unprocessed_points = set(product(range(num_rows), range(num_cols)))
    cost = 0
    while unprocessed_points:
        row, col = unprocessed_points.pop()
        area, u_edges, l_edges, d_edges, r_edges = find_perim_area(row, col, grid,
                                                                   unprocessed_points, num_rows,
                                                                   num_cols)
        num_edges = (
            find_num_edges(u_edges, 0, 1)
            + find_num_edges(l_edges, 1, 0)
            + find_num_edges(d_edges, 0, 1)
            + find_num_edges(r_edges, 1, 0)
        )
        cost += area * num_edges
    print(f'{cost=}')


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
