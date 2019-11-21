"""
    @author: magician
    @date: 2019/11/21
    @file: return_demo.py
"""


def foo1(value):
    """
    foo1
    :param value:
    :return:
    """
    if value:
        return value
    else:
        return None


def foo2(value):
    """
    foo2   Bare return statement implies `return None`
    :param value:
    :return:
    """
    if value:
        return value
    else:
        return


def foo3(value):
    """
    foo3  Missing return statement implies `return None`
    :param value:
    :return:
    """
    if value:
        return value


if __name__ == '__main__':
    print(type(foo1(0)))
    print(type(foo2(0)))
    print(type(foo3(0)))
