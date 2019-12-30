"""
    @author: magician
    @date: 2019/12/30
    @file: super_demo.py
"""
from pprint import pprint


class MyBaseClass(object):
    """
    MyBaseClass
    """
    def __init__(self, value):
        self.value = value


class MyChildClass(MyBaseClass):
    """
    MyChildClass
    """
    def __init__(self):
        MyBaseClass.__init__(self, 5)


class TimesTwo(object):
    """
    TimesTwo
    """
    def __init__(self):
        self.value *= 2


class PlusFive(object):
    """
    PlusFive
    """
    def __init__(self):
        self.value += 5


class OneWay(MyBaseClass, TimesTwo, PlusFive):
    """
    OneWay
    """
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


class AnotherWay(MyBaseClass, PlusFive, TimesTwo):
    """
    AnotherWay
    """
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        TimesTwo.__init__(self)
        PlusFive.__init__(self)


class TimesFive(MyBaseClass):
    """
    TimesFive
    """
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value *= 5


class PlusTwo(MyBaseClass):
    """
    PlusTwo
    """
    def __init__(self, value):
        MyBaseClass.__init__(self, value)
        self.value += 2


class ThisWay(TimesFive, PlusTwo):
    """
    ThisWay
    """
    def __init__(self, value):
        TimesFive.__init__(self, value)
        PlusTwo.__init__(self, value)


class TimesFiveCorrect(MyBaseClass):
    """
    TimesFiveCorrect(python2)
    """
    def __init__(self, value):
        super(TimesFiveCorrect, self).__init__(value)
        self.value *= 5


class PlusTwoCorrect(MyBaseClass):
    """
    PlusTwoCorrect(python2)
    """
    def __init__(self, value):
        super(PlusTwoCorrect, self).__init__(value)
        self.value += 2


class GoodWay(TimesFiveCorrect, PlusTwoCorrect):
    """
    GoodWay(python2)
    """
    def __init__(self, value):
        super(GoodWay, self).__init__(value)


class Explicit(MyBaseClass):
    """
    Explicit
    """
    def __init__(self, value):
        super(__class__, self).__init__(value * 2)


class Implicit(MyBaseClass):
    """
    Implicit
    """
    def __init__(self, value):
        super().__init__(value * 2)


if __name__ == '__main__':
    foo = OneWay(5)
    print('First ordering is (5 * 2) + 5 =', foo.value)

    bar = AnotherWay(5)
    print('Second ordering still is', bar.value)

    foo = ThisWay(5)
    print('Should be (5 * 5) + 2 = 27 but is', foo.value)

    foo = GoodWay(5)
    print('Should be 5 * (5 + 2) = 35 and is', foo.value)

    pprint(GoodWay.mro())

    assert Explicit(10).value == Implicit(10).value
