"""
    @author: magician
    @date: 2019/12/2
    @file: comprehensions_demo.py
"""


if __name__ == '__main__':
    # list comprehensions
    squares = [x * x for x in range(10)]
    print(squares)

    squares = []
    for x in range(10):
        squares.append(x)
    print(squares)

    even_squares = [ x * x for x in range(10) if x % 2 == 0]
    print(even_squares)

    even_squares = []
    for x in range(10):
        if x % 2 == 0:
            even_squares.append(x)
    print(even_squares)

    # set comprehensions
    set_squares = {x * x for x in range(-9, 10)}
    print(set_squares)

    # dict comprehensions
    dict_squares = {x: x * x for x in range(5)}
    print(dict_squares)
