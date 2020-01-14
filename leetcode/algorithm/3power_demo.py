"""
@author: magician
@file:   3power_demo.py
@date:   2020/1/14
"""


def is_power_of_three(n: int) -> bool:
    """
    is_power_of_three
    @param n:
    @return:
    """
    is_three = False

    for i in range(0, n):
        if pow(3, i) == n:
            is_three = True
        elif pow(3, i) > n:
            break
        else:
            continue

    return is_three


if __name__ == '__main__':
    assert is_power_of_three(1) is True
    assert is_power_of_three(3) is True
    assert is_power_of_three(9) is True
    assert is_power_of_three(27) is True
