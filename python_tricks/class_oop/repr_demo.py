"""
    @author: magician
    @date: 2019/11/22
    @file: repr_demo.py
"""
import datetime
from pprint import pprint


class Car:
    """
    Car
    """
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage

    def __repr__(self):
        return '{0} ({1}, {2})'.format(self.__class__.__name__, self.color, self.mileage)

    def __str__(self):
        # return 'a {0} car'.format(self.color)
        return '__str__ for Car'
        # python 2.x
        # return unicode(self).encode('utf-8')

    def __unicode__(self):
        # python 2.x
        return 'a {self.color} car'.format(self=self)


if __name__ == '__main__':
    my_car = Car('red', 37821)
    print(my_car)
    pprint(my_car)
    print(my_car.color, my_car.mileage)

    my_car1 = Car('red', 37821)
    print(my_car1)
    pprint(my_car1)
    print(str(my_car))
    print('{}'.format(my_car))

    # __str__ vs __repr__
    my_car2 = Car('red', 37281)
    print(my_car2)
    print('{}'.format(my_car2))
    pprint(my_car2)
    print(str([my_car2]))
    print(str(my_car2))
    print(repr(my_car2))

    today = datetime.date.today()
    print(str(today))
    print(repr(today))

    # Why Every Class Needs a __repr__
    print(repr(my_car))
    print(my_car)
    print(str(my_car))

    # Python 2.x Differences: __unicode__
    pass
