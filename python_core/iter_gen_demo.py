"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/17
"""
import functools
import os
import psutil

from python_core.decorator_demo import log_execution_time


def is_iterable(param):
    """
    is iterable
    :param param:
    :return:
    """
    try:
        iter(param)
        return True
    except TypeError:
        return False


def show_memory_info(hint):
    """
    show memory info
    :param hint:
    :return:
    """
    pid = os.getpid()
    p = psutil.Process(pid)

    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024
    print('{} memory used: {} MB'.format(hint, memory))

    return memory


def record_memory(func):
    """
    record memory
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        memory1 = show_memory_info(*args)
        func(*args, **kwargs)
        memory2 = show_memory_info(*args)
        print('{} memory used: {} MB'.format(func.__name__, memory2 - memory1))

    return wrapper


@log_execution_time
@record_memory
def test_iterator(*args, **kwargs):
    """
    test iterator
    :param args:
    :param kwargs:
    :return:
    """
    list1 = [i for i in range(100000000)]
    print(sum(list1))

    return True


@log_execution_time
@record_memory
def test_generator(*args, **kwargs):
    """
    test generator
    :param args:
    :param kwargs:
    :return:
    """
    list1 = (i for i in range(100000000))
    print(sum(list1))

    return True


def generator(k):
    """
    generator
    :param k:
    :return:
    """
    i = 1
    while True:
        yield i ** k
        i += 1


gen_1 = generator(1)
gen_3 = generator(3)


def get_sum(n):
    """
    get sum
    :param n:
    :return:
    """
    sum1, sum3 = 0, 0
    for i in range(n):
        next1 = next(gen_1)
        next3 = next(gen_3)
        print('next1 = {}, next3 = {}'.format(next1, next3))
        sum1 += next1
        sum3 += next3
    print(sum1 * sum1, sum3)


def index_normal(l, target):
    """
    index normal
    :param l:
    :param target:
    :return:
    """
    result = []
    for i, num in enumerate(l):
        if num == target:
            result.append(i)

    return result


def index_generator(l, target):
    """
    index generator
    :param l:
    :param target:
    :return:
    """
    for i, num in enumerate(l):
        if num == target:
            yield i


def is_subsequence(a, b):
    """
    is subsequence
    :param a:
    :param b:
    :return:
    """
    b = iter(b)
    print(b)

    gen = (i for i in a)
    print(gen)

    for i in gen:
        print(i)

    gen = ((i in b) for i in a)
    print(gen)

    for i in gen:
        print(i)

    return all(i in b for i in a)


if __name__ == '__main__':
    params = [
        1234,
        '1234',
        [1, 2, 3, 4],
        {1, 2, 3, 4},
        {1: 1, 2: 2, 3: 3, 4: 4},
        (1, 2, 3, 4)
    ]

    for param in params:
        print('{} is iterable? {}'.format(param, is_iterable(param)))

    # test_generator('record')
    # test_iterator('record')

    get_sum(8)

    l, target = [1, 6, 2, 4, 5, 2, 8, 6, 3, 2], 2
    print(index_normal(l, target))
    print(list(index_generator(l, target)))

    print(is_subsequence([1, 3, 5], [1, 2, 3, 4, 5]))
    print(is_subsequence([1, 4, 3], [1, 2, 3, 4, 5]))
