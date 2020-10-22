"""
@author: magician
@file:   variable_demo.py
@date:   2020/10/22
"""
import copy
import weakref


class Gizmo:
    """
    Gizmo
    """

    def __init__(self):
        print('Gizmo id: %d' % id(self))


def f(a, b):
    """
    f
    @param a:
    @param b:
    @return:
    """
    a += b
    return a


class Bus:
    """
    Bus
    """

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


class HauntedBus:
    """
    HauntedBus
    """

    def __init__(self, passengers=[]):
        self.passengers = passengers

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


class TwilightBus:
    """
    TwilightBus
    """

    def __init__(self, passengers=None):
        if passengers is None:
            self.passengers = []
        else:
            self.passengers = list(passengers)

    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)


class Cheese:
    """
    Cheese
    """

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind


class MyList(list):
    """
    list的子类，实例可以作为弱引用的目标
    """
    pass


if __name__ == '__main__':
    # x = Gizmo()
    # y = Gizmo() * 10

    charles = {'name': 'Charles L. Dodgson', 'born': 1832}
    lewis = charles
    print(lewis is charles)
    print(id(lewis), id(charles))
    lewis['balance'] = 950
    print(charles)

    alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
    print(alex == charles)
    print(alex is not charles)

    # tuple
    t1 = (1, 2, [30, 40])
    t2 = (1, 2, [30, 40])
    print(t1 == t2)
    print(id(t1[-1]))
    print(t1[-1].append(99))
    print(id(t1[-1]))
    print(t1 == t2)

    # copy and deepcopy
    l1 = [3, [55, 44], (7, 8, 9)]
    l2 = list(l1)
    # print(l2)
    # print(l2 == l1)
    # print(l2 is l1)
    l1.append(100)
    l1[1].remove(55)
    print('l1:', l1)
    print('l2:', l2)
    l2[1] += [33, 22]
    l2[2] += (10, 11)
    print('l1:', l1)
    print('l2:', l2)

    # bus
    bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
    bus2 = copy.copy(bus1)
    bus3 = copy.deepcopy(bus1)
    print(id(bus1), id(bus2), id(bus3))
    bus1.drop('Bill')
    print(bus2.passengers)
    print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))
    print(bus3.passengers)

    # deepcopy
    a = [10, 20]
    b = [a, 30]
    a.append(b)
    print(a)
    c = copy.deepcopy(a)
    print(c)

    # params
    x, y = 1, 2
    print(x, y)
    print(x, y)
    a, b = [1, 2], [3, 4]
    print(f(a, b))
    print(a, b)
    t, u = (10, 20), (30, 40)
    print(f(t, u))
    print(t, u)

    # HauntedBus
    bus1 = HauntedBus(['Alice', 'Bill'])
    print(bus1.passengers)
    bus1.pick('Charlie')
    bus1.drop('Alice')
    bus2 = HauntedBus()
    bus2.pick('Carrie')
    print(bus2.passengers)
    bus3 = HauntedBus()
    print(bus3.pick('Dave'))
    print(bus2.passengers)
    print(bus2.passengers is bus3.passengers)
    print(bus1.passengers)
    print(dir(HauntedBus.__init__))
    print(HauntedBus.__init__.__defaults__[0] is bus2.passengers)

    # TwilightBus
    basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
    bus = TwilightBus(basketball_team)
    bus.drop('Tina')
    bus.drop('Pat')
    print(basketball_team)

    # del
    s1 = {1, 2, 3}
    s2 = s1


    def bye():
        print('Gone with the wind...')


    ender = weakref.finalize(s1, bye)
    print(ender.alive)
    del s1
    print(ender.alive)
    s2 = 'spam'
    print(ender.alive)

    # weakref
    a_set = {0, 1}
    wref = weakref.ref(a_set)
    print(wref)
    print(wref())
    a_set = {2, 3, 4}
    print(wref())
    print(wref() is None)
    print(wref() is None)

    # Cheese
    stock = weakref.WeakValueDictionary()
    catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]

    for cheese in catalog:
        stock[cheese.kind] = cheese

    print(sorted(stock.keys()))
    del catalog
    print(sorted(stock.keys()))
    del cheese
    print(sorted(stock.keys()))

    a_list = MyList(range(10))
    wref_to_a_list = weakref.ref(a_list)
