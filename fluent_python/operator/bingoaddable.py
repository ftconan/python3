"""
@author: magician
@file:   bingoaddable.py
@date:   2020/12/11
"""
from fluent_python.function_object.first_class_function import BingoCage
from fluent_python.interface.tombola import Tombola


class AddableBingoCage(BingoCage):
    """
    AddableBingoCage
    """

    def __add__(self, other):
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                self_cls = type(self).__name__
                msg = "right operator in += must be {!r} or an iterable"
                raise TypeError(msg.format(self_cls))

        self.load(other_iterable)

        return self

    def load(self, other_iterable):
        pass

    def inspect(self):
        pass

