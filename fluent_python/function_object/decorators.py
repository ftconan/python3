# coding=utf-8

"""
@author: conan
@date: 2018/8/28
"""


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


if __name__ == '__main__':
    # target(return inner function)
    # target()

    # register
    main()
