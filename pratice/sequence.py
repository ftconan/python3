# coding=utf-8

"""
@author: conan
@date: 2018/6/25
"""

if __name__ == '__main__':
    empty_list = list()
    print(empty_list)
    str1 = 'I love you!'
    print(str1)

    fac = (1, 1, 2, 3, 5, 8, 13, 21, 34)
    fac_list = list(fac)
    print(fac_list)

    print(len(empty_list))
    print(len(str1))

    print(max(1, 2, 3, 4, 5))
    print(max([1, 2, 3, 39, -343, 559]))

    print(min([1, 2, 3, 39, -343, 559]))
    print(min((1, 2, 3, 39, -343, 559)))
    print(min('123840'))

    print(sum((3.1, 3.2, 2.2)))
    print(sum((3.1, 3.2, 2.2), 8))

    print(sorted(fac))
    print(list(reversed(fac)))

    print(list(enumerate(fac)))

    a = [1, 2, 3, 4, 5]
    b = [3, 2, 3, 4, 6]
    print(list(zip(a, b)))
