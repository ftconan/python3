"""
@author: magician
@file:   confirm_subclass.py
@date:   2020/1/14
"""


class Meta(type):
    """
    Meta
    """
    def __new__(meta, name, bases, class_dict):
        print(meta, name, bases, class_dict)

        return type.__new__(meta, name, bases, class_dict)


class MyClass(object, metaclass=Meta):
    """
    MyClass
    """
    stuff = 3

    def foo(self):
        pass


class ValidatePolygon(type):
    """
    ValidatePolygon
    """
    def __new__(meta, name, bases, class_dict):
        """
        Don't validate the abstract Polygon class
        @param name:
        @param bases:
        @param class_dict:
        """
        if bases != (object,):
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')

        return type.__new__(meta, name, bases, class_dict)


class Polygon(object, metaclass=ValidatePolygon):
    """
    Polygon
    """
    # Specified by subclasses
    sides = None

    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180


class Triangle(Polygon):
    """
    Triangle
    """
    sides = 3


if __name__ == '__main__':
    print('Before Class')
    try:
        class Line(Polygon):
            """
            Line
            """
            print('Before sides')
            sides = 1
            print('After sides')
    except Exception as e:
        print(e)
    print('After Class')
