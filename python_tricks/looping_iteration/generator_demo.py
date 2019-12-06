"""
    @author: magician
    @date: 2019/12/3
    @file: generator_demo.py
"""


def repeater(value):
    """
    repeater
    :param value:
    :return:
    """
    while True:
        yield value


def repeat_three_times(value):
    """
    repeat_three_times
    :param value:
    :return:
    """
    yield value
    yield value
    yield value


def bounded_repeater(value, max_repeats):
    """
    bounded_repeater
    :param value:
    :param max_repeats:
    :return:
    """
    count = 0
    while True:
        if count >= max_repeats:
            return
        count += 1
        yield value


def bounded_repeater1(value, max_repeats):
    """
    bounded_repeater1
    :param value:
    :param max_repeats:
    :return:
    """
    for i in range(max_repeats):
        yield value


if __name__ == '__main__':
    # Infinite Generator
    # for x in repeater('Hi'):
    #     print(x)

    print(repeater('Hey'))
    generator_obj = repeater('Hey')
    print(next(generator_obj))

    iterator = repeater('Hi')
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))

    # Generators That Stop Generating
    for x in repeat_three_times('Hey there'):
        print(x)

    iterator = repeat_three_times('Hey there')
    next(iterator)
    next(iterator)
    next(iterator)
    try:
        next(iterator)
    except Exception as e:
        print(e)
    try:
        next(iterator)
    except Exception as e:
        print(e)

    for x in bounded_repeater('Hi', 4):
        print(x)

    bounded_repeater1('Hi', 4)
