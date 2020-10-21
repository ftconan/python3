"""
@author: magician
@file:   fibo_demo.py
@date:   2020/10/21
"""
import collections
import functools
import html
import numbers

from fluent_python.decorator.clockdeco import clock


@functools.lru_cache()
@clock
def fibonacci(n):
    """
    fibonacci
    @param n:
    @return:
    """
    if n < 2:
        return n

    return fibonacci(n-2) + fibonacci(n-1)


@functools.singledispatch
def htmlize(obj):
    """
    htmlize
    @param obj:
    @return:
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
@htmlize.register(collections.abc.MutableMapping)
def _(seq):
    inner = '<li>\n<li>'.join(htmlize(item) for item in seq)
    return '<ul>\n<li>' + inner + '</li>\n</ul>'


if __name__ == '__main__':
    print(fibonacci(30))

    # html
    print(htmlize({1, 2, 3}))
    print(htmlize(abs))
    print(htmlize('Heimlich & Co.\n- a game'))
    print(htmlize(42))
    print(htmlize(['alpha', 66, {3, 2, 1}]))
