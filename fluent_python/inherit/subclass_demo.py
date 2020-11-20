"""
@author: magician
@file:   subclass_demo.py
@date:   2020/11/18
"""
import collections


class DoppelDict(dict):
    """
    DoppelDict
    """
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class DoppelDict2(collections.UserDict):
    """
    DoppelDict2
    """
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)


class AnswerDict(dict):
    """
    AnswerDict
    """
    def __getitem__(self, key):
        return 42


class AnswerDict2(collections.UserDict):
    """
    AnswerDict2
    """
    def __getitem__(self, key):
        return 42


if __name__ == '__main__':
    # DoppelDict
    dd = DoppelDict(one=1)
    print(dd)
    dd['two'] = 2
    print(dd)
    dd.update(three=3)
    print(dd)

    # AnswerDict
    ad = AnswerDict(a='foo')
    print(ad['a'])
    d = {}
    d.update(ad)
    print(d['a'])

    # DoppelDict2
    dd = DoppelDict2(one=1)
    print(dd)
    dd['two'] = 2
    print(dd)
    dd.update(three=3)
    print(dd)

    # AnswerDict2
    ad = AnswerDict2(a='foo')
    print(ad['a'])
    d = {}
    d.update(ad)
    print(d['a'])
