"""
@author: magician
@file:   register_subclass.py
@date:   2020/8/4
"""
import json


class Serializable(object):
    """
    Serializable
    """

    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({'args': self.args})


class Point2D(Serializable):
    """
    Point2D
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D({0} {1})'.format(self.x, self.y)


class Deserializable(Serializable):
    """
    Deserializable
    """

    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])


class BetterPoint2D(Deserializable):
    """
    BetterPoint2D
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point2D({0} {1})'.format(self.x, self.y)


class BetterSerializable(object):
    """
    BetterSerializable
    """

    def __init__(self, *args):
        self.args = args

    def serialize(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args,
        })


registry = {}


def register_class(target_class):
    """
    register_class
    @param target_class:
    @return:
    """
    registry[target_class.__name__] = target_class


def deserialize(data):
    """
    deserialize
    @param data:
    @return:
    """
    params = json.loads(data)
    name = params['class']
    target_class = registry[name]

    return target_class(*params['args'])


class EvenBetterPoint2D(BetterSerializable):
    """
    EvenBetterPoint2D
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def __repr__(self):
        return 'EvenBetterPoint2D({0} {1})'.format(self.x, self.y)


class Point3D(BetterSerializable):
    """
    Point3D
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Point3D ({0} {1} {2})'.format(self.x, self.y, self.z)


register_class(EvenBetterPoint2D)
register_class(Point3D)


class Meta(type):
    """
    Meta
    """

    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        register_class(cls)

        return cls


class RegisteredSerializable(BetterSerializable, metaclass=Meta):
    """
    RegisteredSerializable
    """
    pass


class Vector3D(RegisteredSerializable):
    """
    Vector3D
    """

    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Vector3D ({0} {1} {2})'.format(self.x, self.y, self.z)


if __name__ == '__main__':
    # point = Point2D(5, 3)
    # print('Object:    ', point)
    # print('Serialized:', point.serialize())
    #
    # point1 = BetterPoint2D(5, 3)
    # print('Before:    ', point1)
    # data = point1.serialize()
    # print('Serialized:', data)
    # after = BetterPoint2D.deserialize(data)
    # print('After:    ', after)
    #
    # point2 = EvenBetterPoint2D(5, 3)
    # print('Before:    ', point2)
    # data = point2.serialize()
    # print('Serialized:', data)
    # after = deserialize(data)
    # print('After:    ', after)

    # point3 = Point3D(5, 9, -4)
    # print('Before:    ', point3)
    # data3 = point3.serialize()
    # deserialize(data3)
    # print('Serialized:', data3)

    v3 = Vector3D(10, -7, -4)
    print('Before:    ', v3)
    data3 = v3.serialize()
    print('Serialized:', data3)
    print('After:    ', deserialize(data3))
