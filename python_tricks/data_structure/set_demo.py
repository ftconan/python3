"""
    @author: magician
    @date: 2019/11/25
    @file: set_demo.py
"""
from collections import Counter

if __name__ == '__main__':
    # set – Your Go-To Set
    vowels = {'a', 'e', 'i', 'o', 'u'}
    print('e' in vowels)
    letters = set('alice')
    print(letters.intersection(vowels))
    vowels.add('x')
    print(vowels)
    print(len(vowels))

    # frozenset – Immutable Sets
    vowels = frozenset({'a', 'e', 'i', 'o', 'u'})
    try:
        vowels.add('p')
    except Exception as e:
        print(e)
    # Frozensets are hashable and can be used as dictionary keys:
    d = {frozenset({1, 2, 3}): 'hello'}
    print(d[frozenset({1, 2, 3})])

    # collections.Counter – Multisets
    inventory = Counter()
    loot = {'sword': 1, 'bread': 3}
    inventory.update(loot)
    print(inventory)

    more_loot = {'sword': 1, 'apple': 1}
    inventory.update(more_loot)
    print(inventory)

    print(len(inventory))
    print(sum(inventory.values()))
