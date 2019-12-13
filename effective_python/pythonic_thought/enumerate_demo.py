"""
    @author: magician
    @date: 2019/12/13
    @file: enumerate_demo.py
"""
from random import randint


if __name__ == '__main__':
    random_bits = 0
    for i in range(64):
        if randint(0, 1):
            random_bits |= 1 << i

    flavor_list = ['vanilla', 'chocolate', 'pecan', 'strawberry']
    for flavor in flavor_list:
        print('{0} is delicious'.format(flavor))

    for i in range(len(flavor_list)):
        flavor = flavor_list[i]
        print('{0}: {1}'.format(i + 1, flavor))

    for i, flavor in enumerate(flavor_list):
        print('{0}: {1}'.format(i + 1, flavor))
    for i, flavor in enumerate(flavor_list, 1):
        print('{0}: {1}'.format(i, flavor))
