"""
    @author: magician
    @date: 2019/12/18
    @file: sum_of_two.py
"""
import sys


def reverse(x):
    """
    reverse
    :param x:
    :return:
    """
    new_x = 0

    if isinstance(x, int):
        try:
            new_x = int(str(abs(x))[::-1])
            if x < 0:
                new_x = -new_x
            if new_x < pow(-2, 31) or new_x > pow(2, 31):
                new_x = 0
        except:
            new_x = 0

    return new_x


if __name__ == '__main__':
    result1 = reverse(123)
    print(result1)

    result2 = reverse(-1200)
    print(result2)

    result3 = reverse(-9010000)
    print(result3)

    #  [−231,  231 − 1] python int max(9223372036854775807)
    print(sys.maxsize)
    result4 = reverse(1534236469)
    print(result4)
