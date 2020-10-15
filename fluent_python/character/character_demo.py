"""
@author: magician
@file:   character_demo.py
@date:   2020/10/14
"""
import struct

import array

if __name__ == '__main__':
    s = 'café'
    print(len(s))
    b = s.encode('utf-8')
    print(b, len(b))
    print(b.decode('utf-8'))

    cafe = bytes('café', encoding='utf-8')
    print(cafe)
    print(cafe[0])
    print(cafe[:1])
    cafe_arr = bytearray(cafe)
    print(cafe_arr)
    print(cafe_arr[:-1])

    print(bytes.fromhex('31 4B CE A9'))

    numbers = array.array('h', [-2, -1, 0, 1, 2])
    octets = bytes(numbers)
    print(octets)

    # fmt = '<3s3sHH'
    # with open('filter.gif', 'rb') as fp:
    #     img = memoryview(fp.read())
    # header = img[:10]
    # print(bytes(header))
    # print(struct.unpack(fmt, bytes(header)))
    # del header
    # del img

    # codec
    for codec in ['latin_1', 'utf_8', 'utf_16']:
        print(codec, 'El Niño'.encode(codec), sep='\t')
