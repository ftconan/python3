"""
    @author: magician
    @date: 2019/12/19
    @file: key_word_demo.py
"""


def safe_division(number, divisor, ignore_overflow=False, ignore_zero_division=False):
    """
    safe_division
    :param number:
    :param divisor:
    :param ignore_overflow:
    :param ignore_zero_division:
    :return:
    """
    try:
        return number / divisor
    except OverflowError:
        if ignore_overflow:
            return 0
        else:
            raise
    except ZeroDivisionError:
        if ignore_zero_division:
            return float('inf')
        else:
            raise


def safe_division_d(number, divisor, **kwargs):
    """
    safe_division_d
    :param number:
    :param divisor:
    :param kwargs:
    :return:
    """
    # ignore_overflow = kwargs.pop('ignore_overflow', False)
    # ignore_zero_div = kwargs.pop('ignore_zero_division', False)
    if kwargs:
        raise TypeError('Unexpected **kwargs:{0}'.format(kwargs))

    return True


if __name__ == '__main__':
    result = safe_division(1.0, 10**500, True, False)
    print(result)
    result = safe_division(1, 0, False, True)
    print(result)

    try:
        safe_division(1, 10**500, ignore_overflow=True)
    except Exception as e:
        print(e)
    try:
        safe_division(1, 0, ignore_overflow=False)
    except Exception as e:
        print(e)
