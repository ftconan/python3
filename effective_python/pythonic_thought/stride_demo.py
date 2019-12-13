"""
    @author: magician
    @date: 2019/12/13
    @file: stride_demo.py
"""


if __name__ == '__main__':
    a = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
    odds = a[::2]
    evens = a[1::2]
    print(odds)
    print(evens)

    x = b'mongoose'
    y = x[::-1]
    print(y)
    w = '谢谢'
    x = w.encode('utf-8')
    y = x[::-1]
    try:
        z = y.decode('utf-8')
    except Exception as e:
        print(e)

    a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    print(a[::2])
    print(a[::-2])
    print(a[2::2])
    print(a[-2::-2])
    print(a[-2:2:-2])
    print(a[2:2:-2])
    b = a[::2]
    c = b[1:-1]
