"""
@author: magician
@file:   bingo.py
@date:   2020/11/7
"""
import random

from fluent_python.interface.tombola import Tombola


class BingoCage(Tombola):
    """
    BingoCage
    """

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self, *args, **kwargs):
        self.pick()
