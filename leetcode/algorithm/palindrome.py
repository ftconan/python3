"""
    @author: magician
    @date: 2019/12/18
    @file: palindrome.py
"""


def is_palindrome(x: int) -> bool:
    """
    is_palindrome
    :param x:
    :return:
    """
    return bool(str(x) == str(x)[::-1])


if __name__ == '__main__':
    assert is_palindrome(121) is True
