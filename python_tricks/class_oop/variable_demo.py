"""
    @author: magician
    @date: 2019/11/22
    @file: variable_demo.py
"""


class Dog:
    """
    Dog
    """
    num_legs = 4  # Class variable

    def __init__(self, name):
        self.name = name  # Instance variable


class CountedObject:
    """
    CountedObject
    """
    num_instances = 0

    def __init__(self):
        self.__class__.num_instances += 1


class BuggyCountedObject:
    """
    BuggyCountedObject
    """
    num_instances = 0

    def __init__(self):
        self.num_instances += 1


if __name__ == '__main__':
    jack = Dog('Jack')
    jill = Dog('Jill')
    print(jack.name, jill.name)

    print(jack.num_legs, jill.num_legs)
    print(Dog.num_legs)

    try:
        print(Dog.name)
    except Exception as e:
        print(e)

    Dog.num_legs = 6
    print(jack.num_legs, jill.num_legs)

    Dog.num_legs = 4
    jack.num_legs = 6
    print(jack.num_legs, jill.num_legs, Dog.num_legs)

    print(jack.num_legs, jack.__class__.num_legs)

    # A Dog-free Example
    print(CountedObject.num_instances)
    print(CountedObject().num_instances)
    print(CountedObject().num_instances)
    print(CountedObject().num_instances)
    print(CountedObject.num_instances)

    print(BuggyCountedObject.num_instances)
    print(BuggyCountedObject().num_instances)
    print(BuggyCountedObject().num_instances)
    print(BuggyCountedObject().num_instances)
    print(BuggyCountedObject.num_instances)
