"""
@author: magician
@file:   set_demo.py
@date:   2020/10/12
"""
from unicodedata import name


if __name__ == '__main__':
    l = ['spam', 'spam', 'eggs', 'spam']
    print(set(l))
    print(list(set(l)))

    s = {1}
    print(type(s))
    print(s)
    s.pop()
    print(s)

    # frozenset
    print(frozenset(range(10)))

    # setcomps
    print({chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')})
