"""
@author: magician
@file:   lock_demo.py
@date:   2020/8/7
"""
from threading import Thread, Lock


class Counter(object):
    """
    Counter
    """

    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    """
    worker
    @param sensor_index:
    @param how_many:
    @param counter:
    @return:
    """
    for _ in range(how_many):
        counter.increment(1)


class LockingCounter(object):
    """
    LockingCounter
    """

    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset


def run_threads(func, how_many, counter):
    """
    run_threads
    @param func:
    @param how_many:
    @param counter:
    @return:
    """
    threads = []

    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target=func, args=args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    how_many = 10 ** 5
    counter = Counter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))

    counter = LockingCounter()
    run_threads(worker, how_many, counter)
    print('Counter should be %d, found %d' % (5 * how_many, counter.count))
