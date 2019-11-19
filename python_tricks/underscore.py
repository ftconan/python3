"""
    @author: magician
    @date: 2019/11/19
    @file: underscore.py
"""

_MangledGlobal_mangled = 23


class Test:
    """
    Test
    """
    def __init__(self):
        self.foo = 11
        self._bar = 23
        self.__baz = 23


# def make_object(name, class):
#     """
#     make_object
#     SyntaxError: "invalid syntax
#     :param name:
#     :return:
#     """"""
#     pass


def make_object(name, class_):
    """
    make_object
    a single trailing underscore (postfix) is used by convention to avoid naming conflicts with Python keywords.
    :param name:
    :param class_:
    :return:
    """
    pass


class ExtendedTest(Test):
    """
    ExtendedTest
    """
    def __init__(self):
        super().__init__()
        self.foo = 'overridden'
        self._bar = 'overridden'
        self.__baz = 'overridden'


class ManglingTest:
    """
    ManglingTest
    """
    def __init__(self):
        self.__mangled = 'hello'

    def get_mangled(self):
        return self.__mangled


class MangledMethod:
    """
    MangledMethod
    """
    def __method(self):
        return 42

    def call_it(self):
        return self.__method()


class MangledGlobal:
    """
    MangledGlobal
    """
    def test(self):
        __mangled = 0
        return __mangled


class PrefixPostfixTest:
    """
    PrefixPostfixTest
    """
    def __init__(self):
        self.__bam__ = 42


if __name__ == '__main__':
    t = Test()
    print(t.foo)
    # internal variable
    print(t._bar)
    print(dir(t))

    # public function
    def external_func():
        return 23

    # internal function
    def _internal_func():
        return 42

    # from underscore import *
    # external_func()
    # exception: NameError: "name '_internal_func' is not defined"
    # _internal_func()

    # import underscore
    # underscore.external_func()
    # underscore._internal_func()

    # ExtendedTest
    t2 = ExtendedTest()
    print(t2.foo)
    print(t2._bar)
    # AttributeError: "'ExtendedTest' object has no attribute '__baz'"
    # print(t2.__baz)
    print(dir(t2))

    # ManglingTest
    ManglingTest().get_mangled()
    # AttributeError: "'ManglingTest' object has no attribute '__mangled'"
    # print(ManglingTest().__mangled)

    # MangledMethod
    # AttributeError: "'MangledMethod' object has no attribute '__method'"
    # print(MangledMethod().__method())
    print(MangledMethod().call_it())

    # MangledGlobal
    MangledGlobal().test()

    # PrefixPostfixTest
    print(PrefixPostfixTest().__bam__)

    # _
    for _ in range(32):
        print('hello world.')

    car = ('red', 'auto', 12, 3812.4)
    color, _, _, mileage = car
    print(color)
    print(mileage)
    print(_)
    # a = 20 + 3
    # print(a)
    # print(_)
    # l = list()
    # print(l)
    # print(_)
    # _.append(1)
    # _.append(2)
    # _.append(3)
    # print(_)
