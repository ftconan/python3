# coding=utf-8

"""
@author: magician
@date: 2018/8/25
"""
import collections


class StrKeyDict(collections.UserDict):
    """
    key is str
    """
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


if __name__ == '__main__':
    iter_dict = {}
    my_dict = {}
    for key, value in iter_dict.items():
        # best way
        my_dict.setdefault(key, []).append(value)

        # bad way
        if key not in my_dict:
            my_dict[key] = []
        my_dict[key].append(value)