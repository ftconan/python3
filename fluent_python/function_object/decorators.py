# coding=utf-8

"""
@author: conan
@date: 2018/8/28
"""
import functools
import html
import numbers
import time
from collections import abc


def deco(func):
    """
    simple decorator
    :param func:
    :return:  inner function
    """
    def inner():
        print('running inner()')
    return inner


@deco
def target():
    """
    target
    :return:
    """
    print('running target()')


registry = []


def register(func):
    """
    register
    :param func:
    :return:
    """
    print('running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    """
    f1
    :return:
    """
    print('running f1()')


@register
def f2():
    """
    f2
    :return:
    """
    print('running f2()')


def f3():
    """
    f3
    :return:
    """
    print('running f3()')


def main():
    """
    invoke f1, f2, f3
    :return:
    """
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()


def make_averager():
    """
    average number(nonlocal)
    :return:
    """
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        print(total / count)
        return total / count

    return averager


def clock(func):
    """
    clock decorator(record running time)
    :param func:
    :return:
    """
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
            pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(','.join(pairs))
        arg_str = ','.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked


@clock
def snooze(seconds):
    """
    snooze
    :param seconds:
    :return:
    """
    time.sleep(seconds)


@clock
def factorial(n):
    """
    factorial
    :param n:
    :return:
    """
    return 1 if n < 2 else n * factorial(n-1)


@functools.lru_cache()
@clock
def fibonacci(n):
    """
    fibonacci
    :param n:
    :return:
    """
    return n if n < 2 else fibonacci(n - 2) + fibonacci(n - 1)


@functools.singledispatch
def htmlize(obj):
    """
    html analysis
    :param obj:
    :return:
    """
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)


@htmlize.register(str)
def _(text):
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)


@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)


@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)
def _(seq):
    inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'


if __name__ == '__main__':
    # target(return inner function)
    # target()

    # register
    main()

    # average
    avg = make_averager()
    avg(10)
    avg(11)
    avg(12)

    # clock
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! = ', factorial(6))

    # fibonacci(@lru_cache: memory cache)
    print(fibonacci(6))

    # htmlize
    print(htmlize({1, 2, 3}))
    print(htmlize(abs))
    print(htmlize('Heimlich & Co.\n- a game'))
    print(htmlize(42))
    print(htmlize(['alpha', 66, {3, 2, 1}]))
