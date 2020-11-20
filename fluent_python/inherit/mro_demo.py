"""
@author: magician
@file:   mro_demo.py
@date:   2020/11/20
"""
import io
import numbers
import tkinter

from fluent_python.interface.frenchdeck2 import FrenchDeck2


class A:
    """
    A
    """
    def ping(self):
        print('ping:', self)


class B(A):
    """
    B
    """
    def pong(self):
        print('pong:', self)


class C(A):
    """
    C
    """
    def pong(self):
        print('PONG:', self)


class D(B, C):
    """
    D
    """
    def ping(self):
        super().ping()
        print('post-ping:', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)


def print_mro(cls):
    """
    print mro
    @param cls:
    @return:
    """
    print(', '.join(c.__name__ for c in cls.__mro__))


if __name__ == '__main__':
    d = D()
    print(d.pong())
    print(C.pong(d))
    print(D.__mro__)
    print(d.pingpong())

    # print_mro
    print(bool.__mro__)
    print_mro(bool)
    print_mro(FrenchDeck2)
    print_mro(numbers.Integral)
    print_mro(io.BytesIO)
    print_mro(io.TextIOWrapper)

    # tkinter
    print_mro(tkinter.Toplevel)
    print_mro(tkinter.Widget)
    print_mro(tkinter.Button)
    print_mro(tkinter.Entry)
    print_mro(tkinter.Text)
