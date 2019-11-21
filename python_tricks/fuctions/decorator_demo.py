"""
    @author: magician
    @date: 2019/11/21
    @file: decorator_demo.py
"""
import functools


def null_decorator(func):
    """
    null_decorator
    :param func:
    :return:
    """
    return func


def uppercase(func):
    """
    uppercase
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper():
        return func().upper()

    return wrapper


def strong(func):
    """
    strong
    :param func:
    :return:
    """
    def wrapper():
        return '<strong>' + func() + '</strong>'

    return wrapper


def emphasis(func):
    """
    emphasis
    :param func:
    :return:
    """
    def wrapper():
        return '<em>' + func() + '</em>'

    return wrapper


# @null_decorator
# @uppercase
# @strong
# @emphasis
def greet():
    """
    Return a friendly greeting.
    :return:
    """
    return 'Hello!'


def proxy(func):
    """
    proxy
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def trace(func):
    """
    trace
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        print('TRACE: calling {0}() with {1}, {2}'.format(func.__name__, args, kwargs))
        original_result = func(*args, **kwargs)
        print('TRACE: {0}() returned {1}'.format(func.__name__, original_result))

        return original_result

    return wrapper


@trace
def say(name, line):
    """
    say
    :param name:
    :param line:
    :return:
    """
    return '{0}： {1}'.format(name, line)


if __name__ == '__main__':
    # Python Decorator Basic
    # greet = null_decorator(greet)
    # print(greet())

    # print(greet())

    # Decorators Can Modify Behavior
    print(greet())
    # 注释@uppercase
    print(greet)
    print(null_decorator(greet))
    print(uppercase(greet))

    # Applying Multiple Decorators to a Function
    print(greet())
    decorated_greet = strong(emphasis(greet))
    # 注释@strong @emphasis
    print(decorated_greet())

    # Decorating Functions That Accept Argument
    print(say('Jane', 'Hello World'))

    # How to Write “Debuggable” Decorators
    decorated_greet = uppercase(greet)
    # 注释@strong @emphasis
    print(greet.__name__)
    print(greet.__doc__)
    print(decorated_greet.__name__)
    print(decorated_greet.__doc__)


