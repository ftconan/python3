"""
    @author: magician
    @date: 2019/12/13
    @file: generator_demo.py
"""


if __name__ == '__main__':
    value = [len(x) for x in open('/home/magician/Project/python3/data/test.txt')]
    print(value)

    it = (len(x) for x in open('/home/magician/Project/python3/data/test.txt'))
    print(it)
    print(next(it))
    print(next(it))
    roots = ((x, x**0.5) for x in it)
    print(next(roots))
