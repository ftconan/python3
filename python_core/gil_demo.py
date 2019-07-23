"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/23
"""
import dis
import sys
import threading
from threading import Thread

from python_core.decorator_demo import log_execution_time


def count_down(n):
    """
    count_down
    :param n:
    :return:
    """
    while n > 0:
        n -= 1


@log_execution_time
def main():
    """
    main
    :return:
    """
    n = 100000000
    t1 = Thread(target=count_down, args=[n // 2])
    t2 = Thread(target=count_down, args=[n // 2])
    t1.start()
    t2.start()
    t1.join()
    t2.join()


def count_variable():
    """
    count_variable
    :return:
    """
    a = []
    b = a
    print(sys.getrefcount(a))


n = 0
lock = threading.Lock()


def foo():
    """
    foo
    :return:
    """
    global n
    with lock:
        n += 1


def count():
    """
    count
    :return:
    """
    threads = []
    for i in range(100):
        t = threading.Thread(target=foo)
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print(n)


if __name__ == '__main__':
    # main()

    count_variable()

    count()

    dis.dis(foo)
