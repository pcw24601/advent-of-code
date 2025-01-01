# Process time: 28.2 seconds.
import functools
import time
from collections import Counter

import numpy as np


def prune(secrets: np.array) -> np.array:
    return np.mod(secrets, 16777216)


def mix(secrets: np.array, value: int) -> np.array:
    return np.bitwise_xor(secrets, value)


def process_secret(secrets: np.array) -> np.array:
    result = secrets * 64
    secrets = prune(mix(secrets, result))
    result = secrets // 32
    secrets = prune(mix(secrets, result))
    result = secrets * 2048
    secrets = prune(mix(secrets, result))
    return secrets


def sale_price(secret: np.array) -> np.array:
    return np.mod(secret, 10)


def main():
    fname = 'input.txt'
    # fname = 'test2.txt'

    num_iterations = 2000

    secrets = np.loadtxt(fname, dtype=int)
    prices = np.empty((len(secrets), num_iterations, 2), int)
    for secret_num in range(num_iterations):
        prices[:, secret_num, 0] = sale_price(secrets)
        secrets = process_secret(secrets)

    prices[:, 1:, 1] = np.diff(prices[:, :, 0], axis=1)

    num_sellers, num_iterations, _ = prices.shape
    seller_counter_list = []
    # Horrible, double for-loop. There's got to be a performant, vectorised method in numpy :-(.
    for seller in range(num_sellers):
        this_seller_dict = {}
        for it_num in range(4, num_iterations):
            index_ = tuple(prices[seller, it_num-3:it_num+1, 1])
            if index_ in this_seller_dict:
                continue
            this_seller_dict[index_] = prices[seller, it_num, 0]
        seller_counter_list.append(Counter(this_seller_dict))

    grand_counter = functools.reduce(lambda c1, c2: c1 + c2, seller_counter_list)
    max_val = 0
    for key, val in grand_counter.items():
        if val > max_val:
            best_sequence = key
            max_val = val
    print(best_sequence)
    answer = max_val
    print(f'{answer=}')

if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
