"""
    @author: magician
    @date: 2019/11/22
    @file: compare_demo.py
"""


if __name__ == '__main__':
    a = [1, 2, 3]
    b = a
    print(a)
    print(b)
    print(a == b)
    print(a is b)

    c = list(a)
    print(c)
    print(a == c)
    print(a is c)
