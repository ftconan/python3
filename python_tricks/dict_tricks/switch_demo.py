"""
    @author: magician
    @date: 2019/12/6
    @file: switch_demo.py
"""


def myfunc(a, b):
    """
    myfunc
    :param a:
    :param b:
    :return:
    """
    return a + b


def dispatch_if(operator, x, y):
    """
    dispatch_if
    :param operator:
    :param x:
    :param y:
    :return:
    """
    # if operator == 'add':
    #     return x + y
    # elif operator == 'sub':
    #     return x - y
    # elif operator == 'mul':
    #     return x * y
    # elif operator == 'div':
    #     return x / y

    return {
        'add': lambda: x + y,
        'sub': lambda: x - y,
        'mul': lambda: x * y,
        'div': lambda: x / y,
    }.get(operator, lambda: None)()


if __name__ == '__main__':
    funcs = [myfunc]
    print(funcs[0])
    print(funcs[0](2, 3))

    print(dispatch_if('mul', 2, 8))
    print(dispatch_if('unknown', 2, 8))
