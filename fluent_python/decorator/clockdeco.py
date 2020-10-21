"""
@author: magician
@file:   clockdeco.py
@date:   2020/10/21
"""
import functools
import time


def clock(func):
    """
    clock
    @param func:
    @return:
    """
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = []

        if args:
            arg_lst.append(','.join(repr(arg) for arg in args))
        else:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(','.join(pairs))
        arg_str = ','.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))

        return result

    return clocked
