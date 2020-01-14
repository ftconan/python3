"""
@author: magician
@file:   getattr_demo.py
@date:   2020/1/14
"""


class LazyDB(object):
    """
    LazyDB
    """

    def __init__(self):
        self.exists = 5

    def __getattr__(self, name):
        value = 'Value for %s' % name
        setattr(self, name, value)

        return value


class LoggingLazyDB(LazyDB):
    """
    LoggingLazyDB
    """

    def __getattr__(self, name):
        print('Called __getattr__(%s)' % name)

        return super().__getattr__(name)


class ValidateDB(object):
    """
    ValidateDB
    """

    def __init__(self):
        self.exists = 5

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)

            return value


class MissingPropertyDB(object):
    """
    MissingPropertyDB
    """

    def __getattr__(self, name):
        if name == 'bad_name':
            raise AttributeError('%s is missing' % name)


class SavingDB(object):
    """
    SavingDB
    """

    def __setattr__(self, name, value):
        """
        Save some data to the DB log
        @param name:
        @param value:
        @return:
        """
        super().__setattr__(name, value)


class LoggingSavingDB(SavingDB):
    """
    LoggingSavingDB
    """

    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)


class BrokenDictionaryDB(object):
    """
    BrokenDictionaryDB
    """

    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        print('Called __getattribute__(%s)' % name)

        return self._data[name]


class DictionaryDB(object):
    """
    DictionaryDB
    """

    def __init__(self, data):
        self._data = data

    def __getattribute__(self, name):
        data_dict = super().__getattribute__('_data')

        return data_dict[name]


if __name__ == '__main__':
    data = LazyDB()
    print('Before: ', data.__dict__)
    print('foo: ', data.foo)
    print('After: ', data.__dict__)

    data = LoggingLazyDB()
    print('exists: ', data.exists)
    print('foo: ', data.foo)
    print('foo: ', data.foo)

    data = ValidateDB()
    print('exists: ', data.exists)
    print('foo: ', data.foo)
    print('foo: ', data.foo)

    data = MissingPropertyDB()
    try:
        data.bad_name
    except Exception as e:
        print(e)

    data = LoggingLazyDB()
    print('Before: ', data.__dict__)
    print('foo exists: ', hasattr(data, 'foo'))
    print('After: ', data.__dict__)
    print('foo exists: ', hasattr(data, 'foo'))

    data = ValidateDB()
    print('foo exists: ', hasattr(data, 'foo'))
    print('foo exists: ', hasattr(data, 'foo'))

    data = LoggingSavingDB()
    print('Before: ', data.__dict__)
    data.foo = 5
    print('After: ', data.__dict__)
    data.foo = 7
    print('Finally: ', data.__dict__)

    data = BrokenDictionaryDB({'foo': 3})
    try:
        data.foo
    except Exception as e:
        print(e)

    data = DictionaryDB({'foo': 3})
    print(data.foo)
