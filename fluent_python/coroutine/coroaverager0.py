"""
@author: magician
@file:   coroaverager0.py
@date:   2021/12/13
"""


def averager():
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
