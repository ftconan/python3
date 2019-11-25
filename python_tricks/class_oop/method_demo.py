"""
    @author: magician
    @date: 2019/11/25
    @file: method_demo.py
"""
import math


class MyClass:
    """
    MyClass
    """
    def method(self):
        return 'instance method called', self

    @classmethod
    def classmethod(cls):
        return 'class method called', cls

    @staticmethod
    def staticmethod():
        return 'static method called'


class Pizza:
    """
    Pizza
    """
    def __init__(self, ingredients, radius=4):
        self.ingredients = ingredients
        self.radius = radius

    def __repr__(self):
        return 'Pizza({0}, {1})'.format(self.ingredients, self.radius)

    def area(self):
        return self.circle_area(self.radius)

    @staticmethod
    def circle_area(r):
        return r ** 2 * math.pi

    @classmethod
    def margherita(cls):
        return cls(['mozzarella', 'tomatoes'])

    @classmethod
    def prosciutto(cls):
        return cls(['mozzarella', 'tomatoes', 'ham'])


if __name__ == '__main__':
    # Instance Method
    pass

    # Class Method
    pass

    # Static Method
    pass

    # Let’s See Them in Action
    obj = MyClass()
    print(obj.method())
    print(MyClass.method(obj))
    print(obj.classmethod())
    print(obj.staticmethod())

    print(MyClass.classmethod())
    print(MyClass.staticmethod())
    try:
        print(MyClass.method())
    except Exception as e:
        print(e)

    # Delicious Pizza Factories With @classmethod
    print(Pizza(['cheese', 'tomatoes']))
    print(Pizza(['mozzarella', 'tomatoes']))
    print(Pizza(['mozzarella', 'tomatoes', 'ham', 'mushrooms']))
    print(Pizza(['mozzarella'] * 4))

    print(Pizza.margherita())
    print(Pizza.prosciutto())

    # When To Use Static Method
    p = Pizza(['mozzarella', 'tomatoes'], 4)
    print(p)
    print(p.area())
    print(Pizza.circle_area(4))
