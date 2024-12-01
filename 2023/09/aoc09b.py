import numpy as np

fname = r'09/input.txt'
# fname = r'09/test.txt'

arr = np.loadtxt(fname)

# print(np.diff(arr))

def arr_diff(arr):
    if arr.shape[1] == 1:
        return arr  # arr should be all zeroes
    # print(f'{arr.shape=}  \n{arr=}')
    return np.column_stack((arr[:,0] - arr_diff(np.diff(arr))[:,0], arr))

diff_arr = arr_diff(arr)
# print(diff_arr)
print(np.sum(diff_arr[:,0]))