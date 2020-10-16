# coding=utf-8

"""
@author: conan
@date: 2018/8/26
"""
import functools
import operator
import random
from collections import namedtuple
from functools import reduce, partial
from operator import mul, itemgetter, attrgetter, methodcaller

import unicodedata


def factorial(n):
    """
    n阶乘
    :param n:
    :return:
    """
    return 1 if n < 2 else n * factorial(n - 1)


class BingoCage:
    """
    BingoCage
    """

    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    def __call__(self):
        return self.pick()


def upper_case_name(obj):
    """
    upper_case_name
    @param obj:
    @return:
    """
    return ('%s %s' % (obj.first_name, obj.last_name)).upper()


upper_case_name.short_description = 'Customer name'


class C:
    """
    C
    """
    pass


def func():
    """
    func
    @return:
    """
    pass


def tag(name, *content, cls=None, **attrs):
    """
    Generate one or more HTML tags
    :param name:       <img>
    :param content:    hello
    :param cls:        class      hello
    :param attrs:      {'src': 'www.google.com'}
    :return:           <img class='hello' src='www.google.com'>hello</img>
    """
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''

    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


def clip(text: str, max_len: 'int > 80' = 80) -> str:
    """
    在max_len前面或后面的第一个空格处截断文本
    @param text:
    @param max_len:
    @return:
    """
    end = None

    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:
        end = len(text)

    return text[:end].rstrip()


def fact(n):
    """
    fact
    @param n:
    @return:
    """
    return reduce(mul, range(1, n + 1))


if __name__ == '__main__':
    # variable
    fac = factorial
    print(fac)
    print(fac(5))
    print(list(map(fac, range(11))))

    # generator expression
    print(list(map(factorial, range(6))))
    print(list(map(factorial, filter(lambda a: a % 2, range(6)))))

    # modern replacements for map, filter and reduce
    print([factorial(n) for n in range(6)])
    print([factorial(n) for n in range(6) if n % 2])

    # lambda
    fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
    print(sorted(fruits, key=lambda word: word[::-1]))

    # callable
    print([callable(obj) for obj in (abs, str, 13)])

    # __call__
    bingo = BingoCage(range(3))
    print(bingo.pick())
    print(callable(bingo))

    # dir
    print(dir(factorial))
    obj = C()
    print(sorted(set(dir(func)) - set(dir(obj))))

    # html tag
    print(tag('br'))
    print(tag('p', 'hello'))
    print(tag('p', 'hello', 'world'))
    print(tag('p', 'hello', id=33))
    print(tag('p', 'hello', 'world', cls='sidebar'))
    print(tag(content='testing', name="img"))
    my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
    print(tag(**my_tag))

    # clip
    print(clip.__defaults__)
    print(clip.__code__)
    print(clip.__code__.co_varnames)
    print(clip.__code__.co_argcount)

    from inspect import signature

    sig = signature(clip)
    print(sig)
    print(str(sig))
    for name, param in sig.parameters.items():
        print(param.kind, ':', name, '=', param.default)

    print(clip.__annotations__)

    metro_data = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
    ]

    for city in sorted(metro_data, key=itemgetter(1)):
        print(city)

    cc_name = itemgetter(1, 0)
    for city in metro_data:
        print(cc_name(city))
    LatLong = namedtuple('LatLong', 'lat long')
    Metropolis = namedtuple('Metropolis', 'name cc pop coord')
    metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long))
                   for name, cc, pop, (lat, long) in metro_data]
    print(metro_data[0])
    print(metro_areas[0].coord.lat)
    name_lat = attrgetter('name', 'coord.lat')
    for city in sorted(metro_areas, key=attrgetter('coord.lat')):
        print(name_lat(city))

    print([name for name in dir(operator) if not name.startswith('_')])

    # methodcaller
    s = 'The time has come'
    upcase = methodcaller('upper')
    print(upcase(s))
    hiphenate = methodcaller('replace', ' ', '-')
    hiphenate(s)

    # partial
    triple = partial(mul, 3)
    print(triple(7))
    print(list(map(triple, range(1, 10))))

    nfc = functools.partial(unicodedata.normalize, 'NFC')
    s1 = 'café'
    s2 = 'cafe\u0301'
    print(s1, s2)
    print(s1 == s2)
    print(nfc(s1) == nfc(s2))

    picture = functools.partial(tag, 'img', cls='pic-frame')
    print(picture(src='wumpus.jpg'))
    print(picture)
    print(picture.func)
    print(picture.args)
    print(picture.keywords)
