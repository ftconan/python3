"""
    @author: magician
    @date: 2019/12/19
    @file: valid_parentheses.py
"""


def is_valid(s: str) -> bool:
    flag = False

    if len(s) % 2 == 0:
        if len(s) == 2:
            if s == '()' or s == '[]' or s == '{}':
                flag = True
        else:
            s1 = s[:int(len(s) / 2):].replace('()', '').replace('[]', '').replace('{}', '')
            s2 = s[int(len(s) / 2):].replace('()', '').replace('[]', '').replace('{}', '')
            s3 = s2.replace(')', '(').replace(']', '[').replace('}', '{')[::-1]
            print(s1, s2, s3)
            if s1 == s3 and not (')(' in s2 or '][' in s2 or '}{' in s2):
                flag = True

    return flag


if __name__ == '__main__':
    # assert is_valid("()") is True
    # assert is_valid("([])") is True
    # assert is_valid("()[]{}") is True
    # assert is_valid("((") is False
    # assert is_valid("(()(") is False
    assert is_valid("[({(())}[()])]") is True
