"""
    @author: magician
    @date: 2019/12/9
    @file: merge_demo.py
"""


def update(dict1, dict2):
    """
    update
    :param dict1:
    :param dict2:
    :return:
    """
    for key, value in dict2.items():
        dict1[key] = value


if __name__ == '__main__':
    xs = {'a': 1, 'b': 2}
    ys = {'b': 3, 'c': 4}

    zs = {}
    zs.update(xs)
    zs.update(ys)
    print(zs)

    zs = dict(xs, **ys)
    print(zs)

    zs = {**xs, **ys}
    print(zs)
