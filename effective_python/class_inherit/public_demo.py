"""
    @author: magician
    @date: 2019/12/30
    @file: mixin_demo.py
"""


class MyObject(object):
    """
    MyObject
    """
    def __init__(self):
        self.public_field = 5
        self.__private_field = 10

    def get_private_field(self):
        return self.__private_field


class MyParentObject(object):
    """
    MyParentObject
    """
    def __init__(self):
        self.__private_field = 71


class MyChildObject(MyParentObject):
    """
    MyChildObject
    """
    def get_private_field(self):
        return self.__private_field


class MyClass(object):
    """
    MyClass
    This stores the user-supplied value for the object.
    It should coercible to a string. Once assigned for
    the object it should be treated as immutable
    """
    def __init__(self, value):
        self._value = value

    def get_value(self):
        return str(self._value)


class MyIntegerSubclass(MyClass):
    """
    MyIntegerSubclass
    """
    def get_value(self):
        return int(self._MyClass__value)


class ApiClass(object):
    """
    ApiClass
    """
    def __init__(self):
        self._value = 5

    def get(self):
        return self._value


class Child(ApiClass):
    """
    Child
    """
    def __init__(self):
        super().__init__()
        # Conflicts
        self._value = 'hello'


if __name__ == '__main__':
    foo = MyObject()
    assert foo.public_field == 5
    assert foo.get_private_field() == 10
    try:
        print(foo.__private_field)
    except Exception as e:
        print(e)

    baz = MyChildObject()
    try:
        baz.get_private_field()
    except Exception as e:
        print(e)

    assert baz._MyParentObject__private_field == 71
    print(baz.__dict__)

    foo = MyClass(5)
    assert foo.get_value() == '5'

    foo = MyIntegerSubclass(5)
    try:
        assert foo.get_value() == 5
    except Exception as e:
        print(e)

    a = Child()
    print(a.get(), 'and', a._value, 'are different')
