"""
@author: magician
@file:   parallel_computing.py
@date:   2020/8/10
"""
import time
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor


def gcd(pair):
    """
    gcd
    @param pair:
    @return:
    """
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0:
            return i


if __name__ == '__main__':
    numbers = [(1963309, 2265973), (2030677, 3814172),
               (1551645, 2229620), (2039045, 2020802)]
    start = time.time()
    # results = list(map(gcd, numbers))
    # pool = ThreadPoolExecutor(max_workers=4)
    # results = list(pool.map(gcd, numbers))
    pool = ProcessPoolExecutor(max_workers=4)
    results = list(pool.map(gcd, numbers))
    end = time.time()
    print('Took %.3f seconds' % (end - start))
