"""
    @author: magician
    @date: 2019/11/25
    @file: record_demo.py
"""
import dis
from collections import namedtuple
from struct import Struct
from sys import getsizeof
from types import SimpleNamespace
from typing import NamedTuple


class Car:
    """
    Car
    """
    def __init__(self, color, mileage, automatic):
        self.color = color
        self.mileage = mileage
        self.automatic = automatic


# class Car(NamedTuple):
#     """
#     python 3.6+!
#     """
#     color: str
#     mileage: float
#     automatic: bool


if __name__ == '__main__':
    # dict – Simple Data Objects
    car1 = {
        'color': 'red',
        'mileage': 3812.4,
        'automatic': True,
    }
    car2 = {
        'color': 'blue',
        'mileage': 40231,
        'automatic': False,
    }
    # Dicts have a nice repr:
    print(car2)
    # Get mileage:
    print(car2['mileage'])
    # Dicts are mutable:
    car2['mileage'] = 12
    car2['windshield'] = 'broken'
    print(car2)
    # No production against wrong field names, or missing/extra fields:
    car3 = {
        'colr': 'green',
        'automatic': False,
        'windshield': 'broken',
    }

    # tuple – Immutable Groups of Objects
    print(dis.dis(compile("(23, 'a', 'b', 'c')", '', 'eval')))
    print(dis.dis(compile("[23, 'a', 'b', 'c']", '', 'eval')))

    # Fields: color, mileage, automatic
    car1 = ('red', 3812.4, True)
    car2 = ('blue', 40231.0, False)

    # Tuple instances have a nice repr:
    print(car1)
    print(car2)
    # Get mileage:
    print(car2[1])
    # Tuples are immutable:
    try:
        car2[1] = 12
    except Exception as e:
        print(e)
    # No production against missing/extra fields or a wrong order:
    car3 = (3431.5, 'green', True, 'silver')

    # Writing a Custom Class – More Work, More Control
    car1 = Car('red', 3812.4, True)
    car2 = Car('blue', 40231.0, False)
    # Get the mileage:
    print(car2.mileage)
    # Classes are mutable:
    car2.mileage = 12
    car2.windshield = 'broken'
    # String representation is not very powerful(must add a manually written __repr__ method):
    print(car1)
    # collections.namedtuple – Convenient Data Objects
    p1 = namedtuple('Point', 'x y z')(1, 2, 3)
    p2 = (1, 2, 3)
    print(getsizeof(p1))
    print(getsizeof(p2))

    Car = namedtuple('Car', 'color mileage automatic')
    car1 = Car('red', 3812.4, True)
    # Instance have a nice repr:
    print(car1)
    # Accessing fields:
    print(car1.mileage)
    # Fields are immtuable:
    try:
        car1.mileage = 12
    except Exception as e:
        print(e)
    try:
        car1.windshield = 'broken'
    except Exception as e:
        print(e)
    # typing.NamedTuple – Improved Namedtuples
    pass
    # struct.Struct – Serialized C Structs
    MyStruct = Struct('i?f')
    data = MyStruct.pack(23, False, 42.0)
    # All you get is a blob of data:
    print(data)
    # Data blobs can be unpacked again:
    print(MyStruct.unpack(data))

    # types.SimpleNamespace – Fancy Attribute Access
    car1 = SimpleNamespace(color='red',
                           mileage=3812.4,
                           automatic=True)
    # The default repr:
    print(car1)
    # Instances support attribute access and are mutable:
    car1.mileage = 12
    car1.windshield = 'broken'
    del car1.automatic
    print(car1)
