"""
    @author: magician
    @date: 2019/12/13
    @file: closure_demo.py
"""


def sort_priority(values, group):
    """
    sort_priority
    :param values:
    :param group:
    :return:
    """
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)


def sort_priority2(values, group):
    """
    sort_priority2
    :param values:
    :param group:
    :return:
    """
    found = False

    def helper(x):
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)

    return found


def sort_priority3(values, group):
    """
    sort_priority3
    :param values:
    :param group:
    :return:
    """
    found = False

    def helper(x):
        nonlocal found
        if x in group:
            found = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)

    return found


def sort_priority4(values, group):
    """
    sort_priority4(python2)
    :param values:
    :param group:
    :return:
    """
    found = [False]

    def helper(x):
        nonlocal found
        if x in group:
            found[0] = True
            return (0, x)
        return (1, x)
    values.sort(key=helper)

    return found[0]


class Sorter(object):
    """
    Sorter
    """
    def __init__(self, group):
        self.group = group
        self.found = False

    def __call__(self, x):
        if x in self.group:
            self.found = True
            return (0, x)

        return (1, x)


if __name__ == '__main__':
    numbers = [8, 3, 1, 2, 5, 4, 7, 6]
    group = {2, 3, 5, 7}
    sort_priority(numbers, group)
    print(numbers)

    found = sort_priority2(numbers, group)
    print('Found:', found)
    print(numbers)

    sorter = Sorter(group)
    numbers.sort(key=sorter)
    assert sorter.found is True
