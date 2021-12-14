"""
@author: magician
@file:   demo_executor_map.py
@date:   2021/12/14
"""
import time
from concurrent import futures


def display(*args):
    """

    @param args:
    @return:
    """
    print(time.strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    """

    @param n:
    @return:
    """
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    time.sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10


def main():
    """

    @return:
    """
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)
    results = executor.map(loiter, range(5))
    display('results:', results)
    display('Waiting for individual results:')
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


if __name__ == '__main__':
    main()
