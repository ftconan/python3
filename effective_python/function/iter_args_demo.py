"""
    @author: magician
    @date: 2019/12/18
    @file: iter_args_demo.py
"""

NUMBER_PATH = '/home/magician/Project/python3/data/my_numbers.txt'


def normalize(numbers):
    """
    normalize
    :param numbers:
    :return:
    """
    total = sum(numbers)
    result = []

    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result


def read_visits(data_path):
    """
    read_visits
    :param data_path:
    :return:
    """
    with open(data_path) as f:
        for line in f:
            yield int(line)


def normalize_copy(numbers):
    """
    normalize_copy
    :param numbers:
    :return:
    """
    numbers  = list(numbers)
    total = sum(numbers)
    result = []

    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result


def normalize_func(get_iter):
    """
    normalize_func
    :param get_iter:
    :return:
    """
    # new iterator
    total = sum(get_iter())
    result = []

    # new iterator
    for value in get_iter():
        percent = 100 * value / total
        result.append(percent)

    return result


class ReadVisits(object):
    """
    ReadVisits
    """
    def __init__(self, data_path):
        self.data_path = data_path

    def __iter__(self):
        with open(self.data_path) as f:
            for line in f:
                yield int(line)


def normalize_defensive(numbers):
    """
    normalize_defensive
    :param numbers:
    :return:
    """
    if iter(numbers) is iter(numbers):
        raise TypeError('Must supply a container')

    total = sum(numbers)
    result = []

    for value in numbers:
        percent = 100 * value / total
        result.append(percent)

    return result


if __name__ == '__main__':
    visits = [15, 35, 80]
    percentages = normalize(visits)
    print(percentages)

    it = read_visits(NUMBER_PATH)
    print(list(it))
    print(list(it))

    it = read_visits(NUMBER_PATH)
    percentages = normalize_copy(it)
    print(percentages)

    percentages = normalize_func(lambda : read_visits(NUMBER_PATH))
    print(percentages)

    visits = ReadVisits(NUMBER_PATH)
    percentages = normalize(visits)
    print(percentages)

    visits = [15, 35, 80]
    normalize_defensive(visits)
    visits = ReadVisits(NUMBER_PATH)
    normalize_defensive(visits)

    it = iter(visits)
    try:
        normalize_defensive(it)
    except Exception as e:
        print(e)
