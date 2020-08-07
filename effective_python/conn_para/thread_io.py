"""
@author: magician
@file:   thread_io.py
@date:   2020/8/7
"""
import time
from threading import Thread

import select


def factorize(number):
    """
    factorize
    @param number:
    @return:
    """
    for i in range(1, number + 1):
        if number % 1 == 0:
            yield i


class FactorizeThread(Thread):
    """
    FactorizeThread
    """

    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))


def slow_systemcall():
    """
    slow_systemcall
    @return:
    """
    select.select([], [], [], 0.1)


def compute_helicopter_location(index):
    """
    compute_helicopter_location
    @param index:
    @return:
    """
    pass


if __name__ == '__main__':
    numbers = [2139079, 1214759, 1516637, 1852285]
    start = time.time()
    for number in numbers:
        list(factorize(number))
    end = time.time()
    print('Took %.3f seconds' % (end - start))

    start1 = time.time()
    threads = []
    for number in numbers:
        thread = FactorizeThread(number)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    end1 = time.time()
    print('Took %.3f seconds' % (end1 - start1))

    start2 = time.time()
    for _ in range(5):
        slow_systemcall()
    end2 = time.time()
    print('Took %.3f seconds' % (end2 - start2))

    start3 = time.time()
    threads = []
    for _ in range(5):
        thread = Thread(target=slow_systemcall())
        thread.start()
        threads.append(thread)

    for i in range(5):
        compute_helicopter_location(i)
    for thread in threads:
        thread.join()
    end3 = time.time()
