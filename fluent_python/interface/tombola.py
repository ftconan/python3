"""
@author: magician
@file:   tombola.py
@date:   2020/11/7
"""
import abc


class Tombola(abc.ABC):
    """
    Tombola
    """

    _abc_registry = ''

    @abc.abstractmethod
    def load(self, iterable):
        """
        从可迭代对象中添加元素。
        @param iterable:
        @return:
        """

    @abc.abstractmethod
    def pick(self):
        """
        随机删除元素，然后将其返回。
        如果实例为空，这个方法应该抛出`LookupError`。
        @return:
        """

    def loaded(self):
        """
        如果至少有一个元素，返回`True`，否则返回`False`。
        @return:
        """
        return bool(self.inspect())

    def inspect(self):
        """
        返回一个有序元组，由当前元素构成。
        @return:
        """
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break

        self.load(items)

        return tuple(sorted(items))

    @classmethod
    def register(cls, TomboList):
        pass

    @property
    def abc_registry(self):
        return self._abc_registry


class Fake(Tombola):
    """
    Fake
    """

    def pick(self):
        return 13


class MyABC(abc.ABC):
    """
    MyABC
    """

    @classmethod
    @abc.abstractmethod
    def an_abstract_classmethod(cls, **kwargs):
        pass


if __name__ == '__main__':
    f = Fake()
