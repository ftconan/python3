"""
@author: magician
@file:   coroaverager2.py
@date:   2021/12/13
"""
from collections import namedtuple

Result = namedtuple('Result', 'count average')


def averager2():
    """

    @return:
    """
    total = 0.0
    count = 0
    average = None

    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count

    return Result(count, average)
