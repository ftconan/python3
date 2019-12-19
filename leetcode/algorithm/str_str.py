"""
    @author: magician
    @date: 2019/12/19
    @file: rm_element.py
"""


def str_str(haystack: str, needle: str) -> int:
    """
    str_str
    :param self:
    :param haystack:
    :param needle:
    :return:
    """
    if not needle:
        return 0

    return haystack.find(needle)


if __name__ == '__main__':
    assert str_str("hello", "ll") == 2
