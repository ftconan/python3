# coding=utf-8

"""
@author: conan
@date: 2018/7/1
"""

if __name__ == '__main__':
    dict1 = {}
    print(dict1.fromkeys((1, 2, 3)))
    print(dict1.fromkeys((1, 2, 3), 'Number'))
    print(dict1.fromkeys((1, 2, 3), ('one', 'two', 'three')))
    print(dict1.fromkeys((1, 3), 'Number'))

    dict1 = dict1.fromkeys(range(32), 'Number')
    print(dict1)
    for key in dict1.keys():
        print('key: ', key)
    for value in dict1.values():
        print('value: ', value)
    for item in dict1.items():
        print('item: ', item)

    print(dict1.get(32, 'have'))
    print(dict1.get(31, 'have'))

    print((31 in dict1))
    print((32 in dict1))

    dict1.clear()
    print(dict1)

    dict2 = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}
    dict2.pop(2)
    print(dict2)
    dict2.popitem()
    print(dict2)

    dict2.setdefault(5, 'five')
    print(dict2)

    dict3 = {4: 'four'}
    dict2.update(dict3)
    print(dict2)
