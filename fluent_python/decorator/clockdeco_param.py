"""
@author: magician
@file:   clockdeco_param.py
@date:   2020/10/21
"""
import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
    """
    clock
    @param fmt:
    @return:
    """
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result =func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)

            print(fmt.format(**locals()))

            return _result

        return clocked

    return decorate


if __name__ == '__main__':
    @clock()
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)

    @clock('{name}: {elapsed}s')
    def snooze1(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze1(.123)

    @clock('{name}({args}) dt={elapsed:0.3f}s')
    def snooze2(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze2(.123)
