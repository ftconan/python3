"""
    @author: magician
    @date: 2019/11/21
    @file: kwargs_demo.py
"""
import functools


def foo(required, *args, **kwargs):
    """
    foo
    :param required:
    :param args:
    :param kwargs:
    :return:
    """
    print(required)

    if args:
        print(args)
    if kwargs:
        print(kwargs)

    return True


def foo1(x, *args, **kwargs):
    """
    foo1
    :param x:
    :param args:
    :param kwargs:
    :return:
    """
    kwargs['name'] = 'Alice'
    new_args = args + ('extra', )
    # bar(x, *new_args, **kwargs)

    return True


class Car:
    """
    Car
    """
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage


class AlwaysBlueCar(Car):
    """
    AlwaysBlueCar
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = 'blue'


def trace(f):
    """
    trace
    :param f:
    :return:
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        print(f, args, kwargs)
        result = f(*args, **kwargs)
        print(result)

    return decorated_function


@trace
def greet(greeting, name):
    """
    greet
    :param greeting:
    :param name:
    :return:
    """
    return '{}, {}!'.format(greeting, name)


if __name__ == '__main__':
    try:
        foo()
    except Exception as e:
        print(e)

    foo('hello')
    foo('hello', 1, 2, 3)

    foo('hello', 1, 2, 3, key1='value', key2=999)

    # Forwarding Optional or Keyword Argumen
    print(AlwaysBlueCar('green', 48392).color)
    greet('Hello', 'Bob')