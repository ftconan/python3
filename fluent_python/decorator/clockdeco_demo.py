"""
@author: magician
@file:   clockdeco_demo.py
@date:   2020/10/21
"""
import time

from fluent_python.decorator.clockdeco import clock


@clock
def snooze(seconds):
    """
    snooze
    @param seconds:
    @return:
    """
    time.sleep(seconds)


@clock
def factorial(n):
    """
    factorial
    @param n:
    @return:
    """
    return 1 if n < 2 else n * factorial(n-1)


if __name__ == '__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorical(6)')
    print(' 6! =', factorial(6))
