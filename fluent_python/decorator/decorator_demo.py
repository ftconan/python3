"""
@author: magician
@file:   decorator_demo.py
@date:   2020/10/20
"""


def deco(func):
    """
    deco
    @param func:
    @return:
    """
    def inner():
        print('running target()')
    return inner


@deco
def target():
    """
    target
    @return:
    """
    print('running target()')


if __name__ == '__main__':
    print(target())
    print(target)
