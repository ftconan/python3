"""
    @author: magician
    @date: 2019/12/20
    @file: sqrt_demo.py
"""
import math


def my_sqrt(x: int) -> int:
    """
    my_sqrt
    :param x:
    :return:
    """
    return int(math.sqrt(x))


if __name__ == '__main__':
    assert my_sqrt(8) == 2
    assert my_sqrt(0) == 0
