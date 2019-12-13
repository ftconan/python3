"""
    @author: magician
    @date: 2019/12/13
    @file: slice_demo.py
"""


if __name__ == '__main__':
    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    print('First four: ', a[:4])
    print('Last four: ', a[-4:])
    print('Middle two: ', a[3:-3])

    assert a[:5] == a[0:5]
    assert a[5:] == a[5:len(a)]

    print(a[:])
    print(a[:5])
    print(a[:-1])
    print(a[4:])
    print(a[-3:])
    print(a[2:5])
    print(a[2:-1])
    print(a[-3:-1])
    try:
        print(a[20])
    except Exception as e:
        print(e)

    b = a[4:]
    print('Before: ', b)
    b[1] = 99
    print('After: ', b)
    print('No change: ', a)
    print('Before ', a)
    a[2:7] = [99, 22, 14]
    print('After ', a)
    b = a[:]
    assert b == a and b is not a

    b = a
    print('Before ', a)
    a[:] = [101, 102, 103]
    assert a is b
    print('After ', a)
