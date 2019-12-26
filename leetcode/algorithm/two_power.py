"""
    @author: magician
    @date: 2019/12/26
    @file: two_power.py
"""


def is_power_of_two(n: int) -> bool:
    """
    is_power_of_two
    :param n:
    :return:
    """
    i, is_power = 0, False

    while True:
        if pow(2, i) >= n:
            if pow(2, i) == n:
                is_power = True
            break
        else:
            i += 1

    return is_power


if __name__ == '__main__':
    assert is_power_of_two(1) is True
