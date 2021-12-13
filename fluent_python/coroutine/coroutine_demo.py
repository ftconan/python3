"""
@author: magician
@file:   coroutine_demo.py
@date:   2021/12/13
"""
from inspect import getgeneratorstate

from fluent_python.coroutine.coroaverager0 import averager
from fluent_python.coroutine.coroaverager2 import averager2
from fluent_python.coroutine.coroutil import averager1


def simple_coroutine():
    """

    @return:
    """
    print('-> coroutine started')
    x = yield
    print('-> coroutine received:', x)


def simple_coro2(a):
    """

    @param a:
    @return:
    """
    print('-> Started: a =', a)
    b = yield a
    print('-> Received: b =', b)
    c = yield a + b
    print('-> Received: c =', c)


class DemoException(Exception):
    """

    """
    pass


def demo_exc_handling():
    """

    @return:
    """
    print('-> coroutine started')
    while True:
        try:
            x = yield
        except DemoException as e:
            print('*** DemoException handled. Continuing...')
        else:
            print('-> coroutine received: {!r}'.format(x))
    raise RuntimeError('This line should never run.')


def demo_finally():
    """

    @return:
    """
    print('-> coroutine started')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('*** DemoException handled. Continuing...')
            else:
                print('-> coroutine received: {!r}'.format(x))
    finally:
        print('-> coroutine ending')


def chain(*iterable):
    """

    @param iterable:
    @return:
    """
    for it in iterable:
        yield from it


if __name__ == '__main__':
    # my_coro = simple_coroutine()
    # print(my_coro)
    # next(my_coro)
    # try:
    #     my_coro.send(42)
    # except StopIteration as e:
    #     print(e)

    # simple_coro2
    # my_coro2 = simple_coro2(14)
    # print(getgeneratorstate(my_coro2))
    # next(my_coro2)
    # my_coro2.send(28)
    # print(getgeneratorstate(my_coro2))
    # try:
    #     my_coro2.send(99)
    # except StopIteration as e:
    #     print(e)
    # print(getgeneratorstate(my_coro2))

    # coroaverager0
    # coro_avg = averager()
    # next(coro_avg)
    # print(coro_avg.send(10))
    # print(coro_avg.send(30))
    # print(coro_avg.send(5))

    # coroutil
    # coro_avg = averager1()
    # print(coro_avg.send(10))
    # print(coro_avg.send(30))
    # print(coro_avg.send(5))

    # coroutine end
    # coro_avg = averager1()
    # print(coro_avg.send(40))
    # print(coro_avg.send(50))
    # print(coro_avg.send('spam'))

    # DemoException
    # exc_coro = demo_exc_handling()
    # next(exc_coro)
    # exc_coro.send(11)
    # exc_coro.send(22)
    # exc_coro.close()
    # print(getgeneratorstate(exc_coro))
    # exc_coro.throw(DemoException)
    # print(getgeneratorstate(exc_coro))
    # try:
    #     exc_coro.throw(ZeroDivisionError)
    # except Exception as e:
    #     print(e)
    # print(getgeneratorstate(exc_coro))

    # averager2
    # coro_avg = averager2()
    # next(coro_avg)
    # coro_avg.send(10)
    # coro_avg.send(30)
    # coro_avg.send(6.5)
    # try:
    #     coro_avg.send(None)
    # except StopIteration as e:
    #     result = e.value
    #     print(result)

    # yield from
    s = 'ABC'
    t = tuple(range(3))
    print(list(chain(s, t)))
