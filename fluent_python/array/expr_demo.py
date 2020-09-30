"""
@author: magician
@file:   expr_demo.py
@date:   2020/9/30
"""
import array

if __name__ == '__main__':
    # listcomps
    symbols = '$¢£¥€¤'
    print([ord(symbol) for symbol in symbols])

    # filter, map
    print(list(filter(lambda c: c > 127, map(ord, symbols))))

    colors = ['black', 'white']
    sizes = ['S', 'M', 'L']
    print([(color, size) for color in colors for size in sizes])

    # generator
    print(tuple(ord(symbol) for symbol in symbols))
    print(array.array('I', (ord(symbol) for symbol in symbols)))
