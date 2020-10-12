"""
@author: magician
@file:   dict_demo.py
@date:   2020/10/10
"""
import builtins
import collections
import re
import sys
from types import MappingProxyType


class StrKeyDict0(dict):
    """
    StrKeyDict0
    """
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


class StrKeyDict(collections.UserDict):
    """
    StrKeyDict
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
    my_dict = {}
    print(isinstance(my_dict, collections.abc.Mapping))

    # create dict
    a = dict(one=1, two=2, three=3)
    b = {'one': 1, 'two': 2, 'three': 3}
    c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
    d = dict([('two', 2), ('one', 1), ('three', 3)])
    e = dict({'three': 3, 'one': 1, 'two': 2})
    print(a == b == c == d == e)

    # dictcomp
    DIAL_CODES = [
        (86, 'China'),
        (91, 'India'),
        (1, 'United States'),
        (62, 'Indonesia'),
        (55, 'Brazil'),
        (92, 'Pakistan'),
        (880, 'Bangladesh'),
        (234, 'Nigeria'),
        (7, 'Russia'),
        (81, 'Japan'),
    ]
    country_code = {country: code for code, country in DIAL_CODES}
    print(country_code)
    print({code: country.upper() for code, country in DIAL_CODES if code < 66})

    # dict.setdefault
    WORD_RE = re.compile(r'w+')

    # index = {}
    # # index = collections.defaultdict(list())
    # with open(sys.argv[1], encoding='utf-8') as fp:
    #     for line_no, line in enumerate(fp, 1):
    #         for match in WORD_RE.finditer(line):
    #             word = match.group()
    #             column_no = match.start() + 1
    #             location = (line_no, column_no)
    #             index.setdefault(word, []).append(location)
    #             # index[word].append(location)
    #
    # # print word
    # for word in sorted(index, key=str.upper):
    #     print(word, index[word])

    # StrKeyDict0
    d = StrKeyDict0([('2', 'two'), ('4', 'four')])
    print(d['2'])
    print(d[4])
    # print(d[1])

    print(d.get('2'))
    print(d.get(4))
    print(d.get(1, 'N/A'))

    print(2 in d)
    print(1 in d)

    # ChainMap
    pylookup = collections.ChainMap(locals(), globals(), vars(builtins))

    # Counter
    ct = collections.Counter('abracadabra')
    print(ct)
    ct.update('aaaaazzz')
    print(ct.most_common(2))

    # MappingProxyType
    d = {1: 'A'}
    d_proxy = MappingProxyType(d)
    print(d_proxy)
    print(d_proxy[1])
    # d_proxy[2] = 'x'
    d[2] = 'B'
    print(d_proxy)
    print(d_proxy[2])
