# coding=utf-8

"""
@author: conan
@date: 2018/8/26
"""


def factorial(n):
    """
    n阶乘
    :param n:
    :return:
    """
    return 1 if n < 2 else n * factorial(n - 1)


if __name__ == '__main__':
    # generator expression
    print(list(map(factorial, range(6))))
    print(list(map(factorial, filter(lambda a: a % 2, range(6)))))

    # modern replacements for map, filter and reduce
    print([factorial(n) for n in range(6)])
    print([factorial(n) for n in range(6) if n % 2])






