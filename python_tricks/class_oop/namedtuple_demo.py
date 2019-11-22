"""
    @author: magician
    @date: 2019/11/22
    @file: namedtuple_demo.py
"""
from collections import namedtuple

if __name__ == '__main__':
    tup = ('hello', object(), 42)
    print(tup)
    print(tup[2])
    try:
        tup[2] = 23
    except Exception as e:
        print(e)

    # Namedtuples to the Rescue
    # Car = namedtuple('Car', 'color mileage')
    # print('color mileage'.split())
    Car = namedtuple('Car', ['color', 'mileage'])
    my_car = Car('red', 3812.4)
    print(my_car.color)
    print(my_car.mileage)

    print(my_car[0])
    print(tuple(my_car))

    color, mileage = my_car
    print(color, mileage)
    print(*my_car)

    print(my_car)
    try:
        my_car.color = 'blue'
    except Exception as e:
        print(e)

    # Subclassing Namedtuple
    pass
