"""
    @author: magician
    @date: 2019/12/19
    @file: plus_one.py
"""


def plus_one(digits):
    """
    plus_one
    :param digits:
    :return:
    """
    num_str = ''
    num_list = []

    for i in digits:
        num_str += str(i)
    num_str = str(int(num_str) + 1)

    for i in range(len(num_str)):
        num_list.append(int(num_str[i]))

    return num_list


if __name__ == '__main__':
    assert plus_one([1,2,3]) == [1,2,4]
