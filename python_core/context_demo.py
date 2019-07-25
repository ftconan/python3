"""
@file: context_demo.py
@author: magician
@date: 2019/7/23
"""
from contextlib import contextmanager


class FileManager(object):
    """
    FileManager
    """
    def __init__(self, name, mode):
        """
        init
        :param name:
        :param mode:
        """
        print('calling __init__method')
        self.name = name
        self.mode = mode
        self.file = None

    def __enter__(self):
        """
        enter
        :return:
        """
        print('calling __enter__method')
        self.file = open(self.name, self.mode)

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exit
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        print('calling __exit__method')
        if self.file:
            self.file.close()


def write_hello():
    with FileManager('../data/test.txt', 'w+') as f:
        print('ready to write to file')
        f.write('hello world')


class Foo(object):
    """
    Foo
    """
    def __init__(self):
        """
        init
        """
        print('__init__method')

    def __enter__(self):
        """
        enter
        :return:
        """
        print('__enter__method')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exit
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        print('__exit__called')
        if exc_type:
            print('exc_type: {}'.format(exc_type))
            print('exc_val: {}'.format(exc_val))
            print('exc_traceback: {}'.format(exc_tb))
            print('exception handled')

        return True


def context_exception():
    """
    context_exception
    :return:
    """
    with Foo() as obj:
        raise Exception('exception raised').with_traceback(None)


class DBClient(object):
    """
    DBClient
    """
    def __init__(self, host, port):
        """
        init
        :param host:
        :param port:
        """
        self.host = host
        self.port = port

    @staticmethod
    def close():
        """
        close
        :return:
        """
        return True


class DBConnectionManager(object):
    """
    DBConnectionManager
    """
    def __init__(self, hostname, port):
        """
        init
        :param hostname:
        :param port:
        """
        self.hostname = hostname
        self.port = port
        self.connection = None

    def __enter__(self):
        """
        enter
        :return:
        """
        self.connection = DBClient(self.hostname, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        exit
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        """
        self.connection.close()


def db_connect():
    """
    db_connect
    :return:
    """
    with DBConnectionManager('localhost', '8080') as db_client:
        print('host: {}, port: {}'.format(db_client.hostname, db_client.port))
        return True


@contextmanager
def file_manager(name, mode):
    """
    file manager
    :param name:
    :param mode:
    :return:
    """
    try:
        f = open(name, mode)
        yield f
    finally:
        f.close()


def say_hello():
    """
    say_hello
    :return:
    """
    with file_manager('../data/text1.txt', 'w+') as f:
        f.write('hello world')


if __name__ == '__main__':
    write_hello()

    context_exception()

    db_connect()

    say_hello()
