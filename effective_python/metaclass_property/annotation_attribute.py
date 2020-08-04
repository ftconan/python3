"""
@author: magician
@file:   annotation_attribute.py
@date:   2020/8/4
"""


class Field(object):
    """
    Field
    """

    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, instance_type):
        if instance is None:
            return self

        return getattr(instance, self.internal_name, '')

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Customer(object):
    """
    Customer
    """
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


class Meta(type):
    """
    Meta
    """

    def __new__(meta, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)

        return cls


class DatabaseRow(object, metaclass=Meta):
    """
    DatabaseRow
    """
    pass


class Field1(object):
    """
    Field1
    """

    def __init__(self):
        self.name = None
        self.internal_name = None


class BetterCustomer(DatabaseRow):
    """
    BetterCustomer
    """
    first_name = Field1()
    last_name = Field1()
    prefix = Field1()
    suffix = Field1()


if __name__ == '__main__':
    foo = Customer()
    print('Before: ', repr(foo.first_name), foo.__dict__)
    foo.first_name = 'Euclid'
    print('After: ', repr(foo.first_name), foo.__dict__)

    foo1 = BetterCustomer()
    print('Before: ', repr(foo1.first_name), foo1.__dict__)
    foo1.first_name = 'Euluer'
    print('After: ', repr(foo1.first_name), foo1.__dict__)
