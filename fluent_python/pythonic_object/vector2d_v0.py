"""
@author: magician
@file:   vector2d_v0.py
@date:   2020/10/26
"""
import datetime

import math
from array import array


class Vector2d:
    """
    Vector2d
    """
    typecode = 'd'

    def __init__(self, x, y):
        self.__x = float(x)
        self.__y = float(y)

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r},{!r})'.format(class_name, *self)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(array(self.typecode, self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def angle(self):
        return math.atan2(self.y, self.x)

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'

        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)


class Demo:
    """
    Demo
    """

    @classmethod
    def klassmeth(cls, *args):
        return args

    @staticmethod
    def statmeth(*args):
        return args


if __name__ == '__main__':
    # A two-dimensional vector class
    v1 = Vector2d(3, 4)
    print(v1.x, v1.y)
    x, y = v1
    print(x, y)
    print(v1)
    v1_clone = eval(repr(v1))
    v1 = v1_clone
    print(v1)
    octets = bytes(v1)
    print(octets)
    print(abs(v1))
    print(bool(v1), bool(Vector2d(0, 0)))

    # Test of ``.frombytes()`` class method:
    v1_clone = Vector2d.frombytes(bytes(v1))
    print(v1_clone)
    print(v1 == v1_clone)

    # Tests of ``format()`` with Cartesian coordinates:
    print(format(v1))
    print(format(v1, '.2f'))
    print(format(v1, '.3e'))

    # Tests of the ``angle`` method::
    print(Vector2d(0, 0).angle())
    print(Vector2d(1, 0).angle())
    epsilon = 10 ** -8
    print(abs(Vector2d(0, 1).angle() - math.pi/2) < epsilon)
    print(abs(Vector2d(1, 1).angle() - math.pi/4) < epsilon)

    # Tests of ``format()`` with polar coordinates:
    print(format(Vector2d(1, 1), 'p'))
    print(format(Vector2d(1, 1), '.3ep'))
    print(format(Vector2d(1, 1), '0.5fp'))

    # Tests of `x` and `y` read-only properties:
    print(v1.x, v1.y)
    v1.x = 123

    # Tests of hashing:
    v1 = Vector2d(3, 4)
    v2 = Vector2d(3.1, 4.2)
    print(hash(v1), hash(v2))
    print(len(set([v1, v2])))

    # Demo
    print(Demo.klassmeth())
    print(Demo.klassmeth('spam'))
    print(Demo.statmeth())
    print(Demo.statmeth('spam'))

    # format
    br1 = 1 / 2.43
    print(br1)
    print(format(br1, '0.4f'))
    print('1 BRL = {rate:0.2f} USD'.format(rate=br1))

    # format string
    print(format(42, 'b'))
    print(format(2 / 3, '.1%'))
    now = datetime.datetime.now()
    print(format(now, '%H:%M:%S'))
    print("It's {:%I:%M:%p}".format(now))

    # Vector2d
    v1 = Vector2d(3, 4)
    print(format(v1))
    print(v1, '.3f')
    print(v1, '.2f')
    print(v1, '.3e')
    print(format(Vector2d(1, 1), 'p'))
    print(format(Vector2d(1, 1), '.3ep'))
    print(format(Vector2d(1, 1), '0.5fp'))
