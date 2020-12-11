"""
@author: magician
@file:   vector_v5.py
@date:   2020/10/30
"""
import functools
import itertools
import numbers
import operator
import reprlib

import math
from array import array

from fluent_python.pythonic_object.vector2d_v0 import Vector2d


class Vector:
    """
    Vector
    """

    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]

        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return bytes([ord(self.typecode)]) + bytes(self._components)

    def __eq__(self, other):
        # return tuple(self) == tuple(other)
        if isinstance(other, Vector):
            return (len(self) == len(other)) and all(a == b for a, b in zip(self, other))
        else:
            return NotImplemented

    def __ne__(self, other):
        eq_result = self == other
        if eq_result is NotImplemented:
            return NotImplemented
        else:
            return not eq_result

    def __hash__(self):
        hashes = (hash(x) for x in self._components)

        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)

        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __getattr__(self, name):
        cls = type(self)

        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]

        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __setattr__(self, name, value):
        cls = type(self)

        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''

            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)

        super().__setattr__(name, value)

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('h'):
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '<{}>'
        components = (format(c, fmt_spec) for c in coords)

        return outer_fmt.format(','.join(components))

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)

        return cls(memv)

    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __mul__(self, scalar):
        if isinstance(scalar, numbers.Real):
            return Vector(n * scalar for n in self)
        else:
            return NotImplemented

    def __rmul__(self, scalar):
        return self * scalar

    def __matmul__(self, other):
        try:
            return sum(a * b for a, b in zip(self, other))
        except TypeError:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other


if __name__ == '__main__':
    v1 = Vector([3, 4, 5])
    print(len(v1))
    print(v1[0], v1[-1])
    v7 = Vector(range(7))
    print(v7[1:4])

    # add
    v1 = Vector([3, 4, 5])
    print(v1 + (10, 20, 30))
    v2d = Vector2d(1, 2)
    print(v1 + v2d)
    print((10, 20, 30) + v1)
    print(v2d + v1)
    # print(v1 + 1)
    # print(v1 + 'ABC')

    # mul
    v1 = Vector([1.0, 2.0, 3.0])
    print(14 * v1)
    print(v1 * True)
    from fractions import Fraction
    print(v1 * Fraction(1, 3))

    # matmul
    va = Vector([1, 2, 3])
    vz = Vector([5, 6, 7])
    print(va @ vz == 38.0)
    print([10, 20, 30] @ vz)
    # print(va @ 3)

    # eq
    va = Vector([1.0, 2.0, 3.0])
    vb = Vector(range(1, 4))
    print(va == vb)
    vc = Vector([1, 2])
    v2d = Vector2d(1, 2)
    print(vc == v2d)
    t3 = (1, 2, 3)
    print(va == t3)

    # ne
    print(va != vb)
    print(vc != v2d)
    print(va != (1, 2, 3))
