"""
    @author: magician
    @date: 2019/11/22
    @file: namedtuple_demo.py
"""
import json
from collections import namedtuple

Car = namedtuple('Car', 'color mileage')


class MyCarWithMethods(Car):
    """
    MyCarWithMethods
    """
    def hexcolor(self):
        if self.color == 'red':
            return '#ff0000'
        else:
            return '#000000'


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
    c = MyCarWithMethods('red', 1234)
    print(c.hexcolor())

    # add properties
    Car = namedtuple('Car', 'color mileage')
    ElectricCar = namedtuple('ElectricCar', Car._fields + ('charge',))
    print(ElectricCar('red', 1234, 45.0))

    # Built-in Helper Method
    print(my_car._asdict())
    print(json.dumps(my_car._asdict()))
    print(my_car._replace(color='blue'))
    print(Car._make(['red', 999]))

    # When to Use Namedtuple
    pass
