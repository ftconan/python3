"""
    @author: magician
    @date: 2019/11/22
    @file: exception_demo.py
"""


class BaseValidationError(ValueError):
    pass


class NameTooShortError(BaseValidationError):
    pass


class NameTooLongError(BaseValidationError):
    pass


class NameTooCuteError(BaseValidationError):
    pass


def validate(name):
    """
    validate
    :param name:
    :return:
    """
    if len(name) < 10:
        raise NameTooShortError(name)


if __name__ == '__main__':
    try:
        validate('jane')
    except Exception as e:
        print(e)
