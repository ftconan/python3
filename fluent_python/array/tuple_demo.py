"""
@author: magician
@file:   tuple_demo.py
@date:   2020/9/30
"""
import collections

if __name__ == '__main__':
    lax_coordinates = (33.9425, -118.408056)
    city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)
    traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]

    for passport in traveler_ids:
        print('%s/%s' % passport)

    for country, _ in traveler_ids:
        print(country)

    City = collections.namedtuple('City', 'name country population coordinates')
    tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
    print(tokyo)
    print(tokyo.population)
    print(tokyo.coordinates)
    print(tokyo[1])

    print(City._fields)
    LatLong = collections.namedtuple('LatLong', 'lat long')
    delhi_data = ('Delhi NCR', 'IN', 21.935,  LatLong(28.613889, 77.208889))
    delhi = City._make(delhi_data)
    print(delhi._asdict())
