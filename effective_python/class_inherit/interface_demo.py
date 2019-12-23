"""
    @author: magician
    @date: 2019/12/23
    @file: interface_demo.py
"""
from collections import defaultdict


def log_missing():
    """
    log_missing
    :return:
    """
    print('Key added')

    return 0


def increment_with_report(current, increments):
    """
    increment_with_report
    :param current:
    :param increments:
    :return:
    """
    added_count = 0

    def missing():
        nonlocal added_count
        added_count += 1

        return 0

    result = defaultdict(missing, current)
    for key, amount in increments:
        result[key] += amount

    return result, added_count


class CountMissing(object):
    """
    CountMissing
    """
    def __init__(self):
        self.added = 0

    def missing(self):
        self.added += 1

        return 0


class BetterCountMissing(object):
    """
    BetterCountMissing
    """
    def __init__(self):
        self.added = 0

    def __call__(self, *args, **kwargs):
        self.added += 1

        return 0


if __name__ == '__main__':
    # names = ['Socrates', 'Archimedes', 'Plato', 'Aristotle']
    # names.sort(key=lambda x: len(x))
    # print(names)

    current = {'green': 12, 'blue': 3}
    increments = [
        ('red', 5),
        ('blue', 17),
        ('orange', 9),
    ]
    # result = defaultdict(log_missing, current)
    # for key, amount in increments:
    #     result[key] += amount
    # print('After: ', dict(result))

    # result, count = increment_with_report(current, increments)
    # assert count == 2

    # counter = CountMissing()
    # result = defaultdict(counter.missing, current)
    #
    # for key, amount in increments:
    #     result[key] += amount
    # assert counter.added == 2

    # counter = BetterCountMissing()
    # counter()
    # assert callable(counter)

    counter = BetterCountMissing()
    result = defaultdict(counter, current)
    for key, amount in increments:
        result[key] += amount

    assert counter.added == 2
