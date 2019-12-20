"""
    @author: magician
    @date: 2019/12/20
    @file: binary_sum.py
"""


def add_binary(a: str, b: str) -> str:
    """
    add_binary
    :param a:
    :param b:
    :return:
    """
    return str(bin(int(a, 2) + int(b, 2)))[2:]


if __name__ == '__main__':
    assert add_binary('11', '1') == '100'
    assert add_binary('1010', '1011') == '10101'
