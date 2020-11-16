"""
@author: magician
@file:   lotto.py
@date:   2020/11/7
"""
import random

from fluent_python.interface.tombola import Tombola


class LotteryBlower(Tombola):
    """
    LotteryBlower
    """

    def __init__(self, iterable):
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')

        return self._balls.pop(position)

    def loaded(self):
        return bool(self._balls)

    def inspect(self):
        return tuple(sorted(self._balls))
