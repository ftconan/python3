"""
    @author: magician
    @date: 2019/11/25
    @file: dict_demo.py
"""
# import collections
from collections import OrderedDict, defaultdict, ChainMap
from types import MappingProxyType

if __name__ == '__main__':
    # dict – Your Go-To Dictionary
    phonebook = {
        'bob': 7387,
        'alice': 3719,
        'jack': 7052,
    }
    squares = {x: x ** x for x in range(6)}
    print(phonebook['alice'])
    print(squares)

    # collections.OrderedDict – Remember the Insertion Order of Keys
    # d = collections.OrderedDict(one=1, two=2, three=3)
    d = OrderedDict()
    d['one'] = 1
    d['two'] = 2
    d['three'] = 3
    print(d)
    d['four'] = 4
    print(d)
    print(d.keys())

    # collections.defaultdict – Return Default Values for Missing Keys
    dd = defaultdict(list)
    dd['dogs'].append('Rufus')
    dd['dogs'].append('Kathrin')
    dd['dogs'].append('Mr Sniffles')
    print(dd['dogs'])

    # collections.ChainMap – Search Multiple Dictionaries as a Single Mapping
    dict1 = {'one': 1, 'two': 2}
    dict2 = {'three': 3, 'four': 4}
    chain = ChainMap(dict1, dict2)
    print(chain)
    print(chain['three'])
    print(chain['one'])
    print(chain.get('missing', 'missing'))

    # types.MappingProxyType – A Wrapper for Making Read-Only Dictionaries
    writable = {'one': 1, 'two': 2}
    read_only = MappingProxyType(writable)
    print(read_only['one'])
    try:
        read_only['one'] = 23
    except Exception as e:
        print(e)
    writable['one'] = 42
    print(read_only)

    # Dictionaries in Python: Conclusion
    pass
