"""
    @author: magician
    @date: 2019/11/25
    @file: array_demo.py
"""
import array

if __name__ == '__main__':
    arr = ['one', 'two', 'three']
    print(arr[0])
    # Lists have a nice repr:
    print(arr)
    # Lists are mutable:
    arr[1] = 'hello'
    print(arr)

    # del element
    del arr[1]
    print(arr)

    # Lists can hold arbitrary data types:
    arr.append(23)
    print(arr)

    # tuple – Immutable Container
    arr = 'one', 'two', 'three'
    print(arr[0])
    # Tuples have a nice repr:
    print(arr)
    # Tuples are immutable:
    try:
        arr[1] = 'hello'
    except Exception as e:
        print(e)
    # del element
    try:
        del arr[1]
    except Exception as e:
        print(e)
    print(arr + (23,))

    # array.array – Basic Typed Arrays
    arr = array.array('f', (1.0, 1.5, 2.0, 2.5))
    print(arr[1])
    # Arrays have a nice repr:
    print(arr)
    # Arrays are mutable:
    arr[1] = 23.0
    print(arr)
    arr.append(42.0)
    print(arr)
    # Arrays are "typed":
    try:
        arr[1] = 'hello'
    except Exception as e:
        print(e)

    # str – Immutable Arrays of Unicode Characters
    arr = 'abcd'
    print(arr[1])
    print(arr)
    # Strings are immutable:
    try:
        arr[1] = 'e'
    except Exception as e:
        print(e)
    # del element
    try:
        del arr[1]
    except Exception as e:
        print(e)
    # Strings can be unpacked into a list to get a mutable representation:
    print(list('abcd'))
    print(''.join(list('abcd')))

    # Strings are recursive data structures:
    print(type('abc'))
    print(type('abc'[0]))

    # bytes – Immutable Arrays of Single Bytes
    arr = bytes((0, 1, 2, 3))
    print(arr[1])

    # Bytes literals have their own syntax:
    print(arr)
    arr = b'x00x01x02x03'
    # Only valid "bytes" are allowed:
    try:
        print(bytes((0, 300)))
    except Exception as e:
        print(e)
    # Bytes are immutable:
    try:
        arr[1] = 23
    except Exception as e:
        print(e)
    try:
        del arr[1]
    except Exception as e:
        print(e)

    # bytearray – Mutable Arrays of Single Bytes
    arr = bytearray((0, 1, 2, 3))
    print(arr[1])
    # The bytearray repr:
    arr[1] = 23
    print(arr)
    # Bytearrays can grow and shrink in size:
    del arr[1]
    print(arr)
    arr.append(42)
    print(arr)
    # Bytearrays can only hold "bytes"(integers in the range 0<=x<=255)
    try:
        arr[1] = 'hello'
    except Exception as e:
        print(e)
    try:
        arr[1] = 300
    except Exception as e:
        print(e)
    # Bytearrays can be converted back into bytes objects:(This will copy the data)
    print(bytes(arr))
