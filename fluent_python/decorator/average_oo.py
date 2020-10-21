"""
@author: magician
@file:   average_oo.py
@date:   2020/10/20
"""


class Averager():
    """
    Averager
    """

    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)

        return total / len(self.series)


def make_averager():
    """
    make_averager
    @return:
    """
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)

        return total / len(series)

    return averager


def make_averager1():
    """
    make_averager1
    @return:
    """
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total

        count += 1
        total += new_value
        return total / count

    return averager


if __name__ == '__main__':
    avg = Averager()
    print(avg(10))
    print(avg(11))
    print(avg(12))

    avg1 = make_averager()
    print(avg1(10))
    print(avg1(11))
    print(avg1(12))
    print(avg1.__code__.co_varnames)
    print(avg1.__code__.co_freevars)
    print(avg1.__closure__)
    print(avg1.__closure__[0].cell_contents)

    avg2 = make_averager1()
    print(avg2(10))
