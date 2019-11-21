"""
    @author: magician
    @date: 2019/11/21
    @file: unpack_demo.py
"""


def print_vector(x, y, z):
    """
    print_vector
    :param x:
    :param y:
    :param z:
    :return:
    """
    print('<%s, %s, %s>' % (x, y, z))

    return True


if __name__ == '__main__':
    print_vector(0, 1, 0)

    tuple_vec = (1, 0, 1)
    list_vec = [1, 0, 1]
    print_vector(tuple_vec[0],
                 tuple_vec[1],
                 tuple_vec[2])

    print_vector(*tuple_vec)
    print_vector(*list_vec)

    genexpr = (x * x for x in range(3))
    print_vector(*genexpr)

    dict_vec = {'y': 0, 'z': 1, 'x': 1}
    print_vector(**dict_vec)
    print_vector(*dict_vec)
