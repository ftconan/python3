"""
    @author: magician
    @date: 2019/11/22
    @file: copy_demo.py
"""
import copy


class Point:
    """
    Point
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point({0}, {1})'.format(self.x, self.y)


class Rectangle:
    """
    Rectangle
    """
    def __init__(self, topleft, bottomright):
        self.topleft = topleft
        self.bottomright = bottomright

    def __repr__(self):
        return 'Rectangle({0}, {1})'.format(self.topleft, self.bottomright)


if __name__ == '__main__':
    # Making Shallow Copies
    xs = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    ys = list(xs)  # Make a shallow copy
    print(xs)
    print(ys)

    xs.append(['new sublist'])
    print(xs)
    print(ys)

    # xs[1][0] = 'X'
    print(xs)
    print(ys)

    # Making Deep Copies
    zs = copy.deepcopy(xs)
    print(xs)
    print(zs)
    xs[1][0] = 'X'
    print(xs)
    print(zs)

    # Copying Arbitrary Objects
    a = Point(23, 42)
    b = copy.copy(a)
    print(a)
    print(b)
    print(a is b)

    rect = Rectangle(Point(0, 1), Point(5, 6))
    srect = copy.copy(rect)
    print(rect)
    print(srect)
    print(rect is srect)

    rect.topleft.x = 999
    print(rect)
    print(srect)

    drect = copy.deepcopy(srect)
    drect.topleft.x = 222
    print(drect)
    print(rect)
    print(srect)
