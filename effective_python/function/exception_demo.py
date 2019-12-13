"""
    @author: magician
    @date: 2019/12/13
    @file: exception_demo.py
"""


def divide(a, b):
    """
    divide
    :param a:
    :param b:
    :return:
    """
    try:
        return a / b
    except ZeroDivisionError:
        return None


def divide1(a, b):
    """
    divide1
    :param a:
    :param b:
    :return:
    """
    try:
        return True, a / b
    except ZeroDivisionError:
        return False, None


def divide2(a, b):
    """
    divide2
    :param a:
    :param b:
    :return:
    """
    try:
        return a / b
    except ZeroDivisionError as e:
        raise ValueError('Invalid inputs') from e


if __name__ == '__main__':
    x, y = 0, 5
    result = divide(x, y)
    if not result:
        print('Invalid inputs')

    success, result = divide1(x, y)
    if not success:
        print('Invalid inputs')

    _, result = divide1(x, y)
    if not result:
        print('Invalid inputs')

    x, y = 5, 2
    try:
        result = divide(x, y)
    except ValueError:
        print('Invalid inputs')
    else:
        print('Result is %.1f' % result)
