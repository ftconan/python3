"""
    @author: magician
    @date: 2019/12/3
    @file: iterator_demo.py
"""


class RepeaterIterator(object):
    """
    RepeaterIterator
    """

    def __init__(self, source):
        self.source = source

    def __next__(self):
        return self.source.value


class Repeater(object):
    """
    Repeater
    """

    def __init__(self, value):
        self.value = value

    def __iter__(self):
        # return RepeaterIterator(self)
        return self

    def __next__(self):
        return self.value


class BoundedRepeater:
    """
    BoundedRepeater
    """

    def __init__(self, value, max_repeats):
        self.value = value
        self.max_repeats = max_repeats
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_repeats:
            raise StopIteration
        self.count += 1

        return self.value


class InfiniteRepeater(object):
    """
    InfiniteRepeater
    """

    def __init__(self, value):
        self.value = value

    def __iter__(self):
        return self

    def __next__(self):
        return self.value

    def next(self):
        """
        Python 2 compatibility
        :return:
        """
        return self.__next__()


if __name__ == '__main__':
    # Iterating Forever
    repeater = Repeater('Hello')
    # for item in repeater:
    #     print(item)

    # How do for-in loops work in Python
    # iterator = repeater.__iter__()
    # while True:
    #     item = iterator.__next__()
    #     print(item)

    iterator = iter(repeater)
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))

    # A Simpler Iterator Class
    pass

    # Who Wants to Iterate Forever
    numbers = [1, 2, 3]
    for n in numbers:
        print(n)
    my_list = [1, 2, 3]
    iterator = iter(my_list)
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    try:
        next(iterator)
    except Exception as e:
        print(e)

    bounded_repeater = BoundedRepeater('Hello', 3)
    for item in bounded_repeater:
        print(item)
    iterator = iter(bounded_repeater)
    while True:
        try:
            item = next(iterator)
        except StopIteration:
            break
        print(item)

    # Python 2.x Compatibility
    pass
