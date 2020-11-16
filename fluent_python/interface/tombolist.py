"""
@author: magician
@file:   tombolist.py
@date:   2020/11/7
"""
import random

from fluent_python.interface.tombola import Tombola


@Tombola.register
class TomboList(list):
    """
    TomboList
    """

    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')

    load = list.extend

    def loaded(self):
        return bool(self)

    def inspect(self):
        return tuple(sorted(self))


Tombola.register(TomboList)


if __name__ == '__main__':
    # print(issubclass(TomboList, Tombola))
    t = TomboList(range(100))
    print(isinstance(t, Tombola))
    print(Tombola.__mro__)
