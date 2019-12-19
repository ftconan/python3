"""
    @author: magician
    @date: 2019/12/19
    @file: valid_parentheses.py
"""


def is_valid(s: str) -> bool:
    """
    is_valid
    :param s:
    :return:
    """
    while '()' in s or '[]' in s or '{}' in s:
        s = s.replace('()', '')
        s = s.replace('[]', '')
        s = s.replace('{}', '')

    return s == ''


if __name__ == '__main__':
    assert is_valid("()") is True
    assert is_valid("([])") is True
    assert is_valid("()[]{}") is True
    assert is_valid("((") is False
    assert is_valid("(()(") is False
    assert is_valid("[({(())}[()])]") is True
