"""
@author: magician
@file:   coroutil.py
@date:   2021/12/13
"""
import functools


def coroutine(func):
    """

    @param func:
    @return:
    """

    @functools.wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)

        return gen

    return primer


@coroutine
def averager1():
    """

    @return:
    """
    total = 0.0
    count = 0
    average = None

    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
