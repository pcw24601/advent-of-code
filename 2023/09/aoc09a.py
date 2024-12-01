import numpy as np

fname = r'09/input.txt'
# fname = r'09/test.txt'

arr = np.loadtxt(fname)

# print(np.diff(arr))

def arr_diff(arr):
    if arr.shape[1] == 1:
        return arr  # arr should be all zeroes
    # this_arr_diff = arr_diff(arr)
    # print(f'{arr.shape=}  \n{arr=}')
    return np.column_stack((arr, arr[:,-1] + arr_diff(np.diff(arr))[:,-1]))

print(np.sum(arr_diff(arr)[:,-1]))