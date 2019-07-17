"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/15
"""
import functools
import time


def func(message):
    """
    func
    :param message:
    :return:
    """
    print('Got a message:{}'.format(message))


def get_message(message):
    """
    get message
    :param message:
    :return:
    """
    return 'Got a message: ' + message


def root_call(func, message):
    """
    root call
    :param func:
    :param message:
    :return:
    """
    print(func(message))


def new_func(message):
    """
    new func
    :param message:
    :return:
    """

    def get_message(message):
        """
        get message
        :param message:
        :return:
        """
        print('Got a message:{}'.format(message))

    return get_message(message)


def func_closure():
    """
    func closure
    :return:
    """

    def get_message(message):
        print('Got a message:{}'.format(message))

    return get_message


def my_decorator(func1):
    """
    my decorator
    :param func1:
    :return:
    """

    def wrapper():
        """
        wrapper
        :return:
        """
        print('wrapper of decorator')
        func1()

    return wrapper


def greet():
    """
    greet
    :return:
    """
    print('hello world')


def my_decorator1(func2):
    """
    my decorator1
    :param func2:
    :return:
    """
    def wrapper():
        """
        wrapper
        :return:
        """
        print('wrapper of decorator')
        func2()

    return wrapper


@my_decorator1
def greet3():
    """
    greet3
    :return:
    """
    print('hello world')


def my_decorator3(func4):
    """
    my decorator3
    :param func4:
    :return:
    """
    def wrapper(message):
        """
        wrapper
        :param message:
        :return:
        """
        print('wrapper of decorator')
        func4(message)

    return wrapper


@my_decorator3
def greet4(message):
    """
    greet4
    :param message:
    :return:
    """
    print(message)


def my_decorator5(func5):
    """
    my decorator5
    :param func5:
    :return:
    """
    def wrapper(*args, **kwargs):
        """
        wrapper
        :param args:
        :param kwargs:
        :return:
        """
        print('wrapper of decorator')
        func5(*args, **kwargs)

    return wrapper


def repeat(num):
    """
    repeat
    :param num:
    :return:
    """
    def my_decorator(func):
        """
        my decorator
        :param func:
        :return:
        """
        def wrapper(*args, **kwargs):
            """
            wrapper
            :param args:
            :param kwargs:
            :return:
            """
            for i in range(num):
                print('wrapper of decorator')
                func(*args, **kwargs)

        return wrapper

    return my_decorator


@repeat(4)
def greet6(message):
    """
    greet6
    :param message:
    :return:
    """
    print(message)


def my_decorator6(func6):
    """
    my decorator6
    :param func6:
    :return:
    """
    @functools.wraps(func6)
    def wrapper(*args, **kwargs):
        """
        wrapper
        :param args:
        :param kwargs:
        :return:
        """
        print('wrapper of decorator')
        func6(*args, **kwargs)

    return wrapper


@my_decorator6
def greet7(message):
    """
    greet7
    :param message:
    :return:
    """
    print(message)


class Count:
    """
    Count
    """
    def __init__(self, func):
        """
        init
        :param func:
        """
        self.func = func
        self.num_calls = 0

    def __call__(self, *args, **kwargs):
        """
        call
        :param args:
        :param kwargs:
        :return:
        """
        self.num_calls += 1
        print('num of calls is: {}'.format(self.num_calls))

        return self.func(*args, **kwargs)


@Count
def example():
    """
    example
    :return:
    """
    print('hello world')


def new_decorator1(func0):
    """
    new decorator1
    :param func0:
    :return:
    """
    @functools.wraps(func0)
    def wrapper(*args, **kwargs):
        """
        wrapper
        :param args:
        :param kwargs:
        :return:
        """
        print('execute decorator1')
        func0(*args, **kwargs)

    return wrapper


def new_decorator2(fun):
    """
    new decorator2
    :param fun:
    :return:
    """
    @functools.wraps(fun)
    def wrapper(*args, **kwargs):
        print('execute decorator2')
        func(*args, **kwargs)

    return wrapper


@new_decorator1
@new_decorator2
def new_greet(message):
    """
    new greet
    :param message:
    :return:
    """
    print(message)


def check_user_logged_in(request):
    """
    check user logged in
    :param request:
    :return:
    """
    if not request:
        return False

    return True


def authenticate(new_func1):
    """
    authenticate
    :param new_func1:
    :return:
    """
    @functools.wraps(new_func1)
    def wrapper(*args, **kwargs):
        request = args[0]
        if check_user_logged_in(request):
            return new_func1(*args, **kwargs)
        else:
            raise Exception('Authentication failed')

    return wrapper


def log_execution_time(new_func2):
    """
    log execution time
    :param new_func2:
    :return:
    """
    @functools.wraps(new_func2)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = new_func2(*args, **kwargs)
        end = time.perf_counter()
        print('{} took {} ms'.format(func.__name__, (end - start) * 1000))

    return wrapper


@log_execution_time
def calculate_similarity(items):
    """
    calculate similarity
    :param items:
    :return:
    """
    return items


def validation_check(input):
    """
    validation check
    :param input:
    :return:
    """
    @functools.wraps(input)
    def wrapper(*args, **kwargs):
        pass

    return wrapper


@validation_check
def neural_network_training(param1, param2, **kwargs):
    """
    neural network training
    :param param1:
    :param param2:
    :param kwargs:
    :return:
    """
    return True


@functools.lru_cache
def check(param1, **kwargs):
    """
    check
    :param param1:
    :param kwargs:
    :return:
    """
    return True


if __name__ == '__main__':
    send_message = func
    send_message('hello world')

    root_call(get_message, 'hello world')

    new_func('hello world')

    send_message = func_closure()
    send_message('hello world')

    greet1 = my_decorator(greet)
    greet1()

    greet3()

    greet4('hello world')

    greet6('hello world')

    print(greet6.__name__)
    help(greet6)

    print(greet7.__name__)

    example()
    example()

    new_greet('hello world')
