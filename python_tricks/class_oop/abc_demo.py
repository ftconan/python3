"""
    @author: magician
    @date: 2019/11/22
    @file: abc_demo.py
"""
from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    """
    Base
    """
    @abstractmethod
    def foo(self):
        # raise NotImplementedError()
        pass

    @abstractmethod
    def bar(self):
        # raise NotImplementedError()
        pass


class Concrete(Base):
    """
    Concrete
    """
    def foo(self):
        # return 'foo() called'
        pass

    # Oh no, we forgot to override bar()...
    # def bar(self):
    #     return "bar() called"


if __name__ == '__main__':
    try:
        b = Base()
        b.foo()
    except Exception as e:
        print(e)

    try:
        c = Concrete()
        c.foo()
        c.bar()
    except Exception as err:
        print(err)

    assert issubclass(Concrete, Base)
