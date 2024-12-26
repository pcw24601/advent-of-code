# Process time: 0.0459 seconds.
import time
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



def main():
    fname = 'input.txt'
    # fname = 'test.txt'

    secrets = np.loadtxt(fname, dtype=int)

    for _ in range(2000):
        secrets = process_secret(secrets)

    answer = sum(secrets)
    print(f'{answer=}')
    pass


if __name__ == '__main__':
    start_time = time.process_time()
    main()
    print(f"Process time: {time.process_time() - start_time:.03g} seconds.")
