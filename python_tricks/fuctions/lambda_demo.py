"""
    @author: magician
    @date: 2019/11/21
    @file: lambda_demo.py
"""


def add(x, y):
    """
    add
    :param x:
    :param y:
    :return:
    """
    return x + y


def make_adder(n):
    """
    make_adder
    :param n:
    :return:
    """
    return lambda x: x + n


class Car:
    """
    Harmful Car
    """
    rev = lambda self: print('Wroom!')
    crash = lambda self: print('Boom!')


if __name__ == '__main__':
    add = lambda x, y: x + y
    print(add(5, 3))
    print(add(5, 3))

    print((lambda x, y: x + y)(5, 3))

    # Lambdas You Can Use
    tuples = [(1, 'd'), (2, 'b'), (4, 'a'), (3, 'c')]
    sorted(tuples, key=lambda x: x[1])
    print(tuples)

    print(sorted(range(-5, 6), key=lambda x: x * x))
    plus_3 = make_adder(3)
    plus_5 = make_adder(5)
    print(plus_3(4))
    print(plus_5(4))

    # But Maybe You Shouldn’t
    my_car = Car()
    my_car.crash()

    # Harmful
    print(list(filter(lambda x: x % 2 == 0, range(16))))

    # Better:
    print([x for x in range(16) if x % 2 == 0])
