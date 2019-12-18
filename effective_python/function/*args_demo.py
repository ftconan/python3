"""
    @author: magician
    @date: 2019/12/18
    @file: *args_demo.py
"""


def log(message, *values):
    """
    log
    :param message:
    :param values:
    :return:
    """
    if not values:
        print(message)
    else:
        values_str = ', '.join(str(x) for x in values)
        print('{0}: {1}'.format(message, values_str))

    return True


def my_generator():
    """
    my_generator
    :return:
    """
    for i in range(10):
        yield i


def my_func(*args):
    """
    my_func
    :param args:
    :return:
    """
    print(args)


def log1(sequence, message, *values):
    """
    log1
    :param sequence:
    :param message:
    :param values:
    :return:
    """
    if not values:
        print('{0}: {1}'.format(sequence, message))
    else:
        values_str = ', '.join(str(x) for x in values)
        print('{0}: {1}: {2}'.format(sequence, message, values_str))

    return True


if __name__ == '__main__':
    log('My numbers are', [1, 2])
    log('Hi there', [])

    log('My numbers are', 1, 2)
    log('Hi there')

    favorites = [7, 33, 99]
    log('Favorite colors', *favorites)

    it = my_generator()
    my_func(*it)

    log1(1, 'Favorites', 7, 33)
    log1('Favorite numbers', 7, 33)