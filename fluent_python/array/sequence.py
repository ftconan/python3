# coding=utf-8

"""
@author: conan
@date: 2018/8/22
"""
import bisect
from array import array
from collections import namedtuple, deque
from random import random

import numpy

if __name__ == '__main__':
    City = namedtuple('City', 'name country population coordinates')
    tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.791667))
    print(tokyo)
    print(tokyo.population)
    print(tokyo.coordinates)
    print(tokyo[1])

    print(City._fields)
    LatLong = namedtuple('LatLong', 'lat long')
    delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
    delhi = City._make(delhi_data)
    print(delhi._asdict())

    for key, value in delhi._asdict().items():
        print(key + ':', value)

    # puzzler tuple
    t = (1, 2, [30, 40])
    try:
        t[2] += [50, 60]
    except Exception as e:
        print(e)
    print(t)

    # bool
    print(1 == 1.0)

    # bisect
    def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
        i = bisect.bisect(breakpoints, score)
        return grades[i]
    print([grade(score) for score in [33, 99, 77, 70, 89, 90, 100]])

    # array
    # floats = array('d', (random() for i in range(10 ** 7)))
    # print(floats[-1])
    # fp = open('floats.bin', 'wb')
    # floats.tofile(fp)
    # fp.close()
    # floats2 = array('d')
    # fp = open('floats.bin', 'rb')
    # floats2.fromfile(fp, 10 ** 7)
    # fp.close()
    # print(floats2[-1])
    # print(floats2 == floats)

    # memoryview
    numbers = array('h', [-2, -1, 0, 1, 2])
    memv = memoryview(numbers)
    print(len(memv))
    print(memv[0])
    memv_oct = memv.cast('B')
    print(memv_oct.tolist())
    memv_oct[5] = 4
    print(numbers)

    # numpy and scipy
    a = numpy.arange(12)
    print(a)
    print(type(a))
    print(a.shape)
    a.shape = 3, 4
    print(a)
    print(a[2])
    print(a[2, 1])
    print(a[:, 1])
    print(a.transpose())
    # floats = numpy.loadtxt('floatss-10M-lines.txt')
    # print(floats[-3:])
    # floats *= .5
    # from time import perf_counter as pc
    # t0 = pc()
    # floats /= 3
    # print(pc() - t0)
    # numpy.save('floats-10M', floats)
    # floats2 = numpy.load('floats-10M.npy', 'r+')
    # floats2 *= 6
    # print(floats2[-3:])

    # deque
    dq = deque(range(10), maxlen=10)
    print(dq)
    # right -> left
    dq.rotate(3)
    print(dq)
    # left -> right
    dq.rotate(-4)
    print(dq)
    dq.appendleft(-1)
    print(dq)
    dq.extend([11, 22, 33])
    print(dq)
    dq.extendleft([10, 20, 30, 40])
    print(dq)
