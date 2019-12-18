"""
    @author: magician
    @date: 2019/12/18
    @file: doc_demo.py
"""
import json
import time
from datetime import datetime


def log(message, when=None):
    """
    Log a message with a timestamp.
    :param message: Message to print.
    :param when: datetime of when the message occured.
                 Defaults to the present time.
    :return:
    """
    when = datetime.now() if when is None else when
    print('{0}: {1}'.format(when, message))

    return True


def decode(data, default=None):
    """
    Load JSON data from a string.
    :param data: JSON data to decode.
    :param default: Value to return if decoding fails.
                    Default to an empty dictionary.
    :return:
    """
    if default is None:
        default = {}

    try:
        return json.loads(data)
    except ValueError:
        return default


if __name__ == '__main__':
    log('Hi there!')
    time.sleep(0.1)
    log('Hi again!')

    foo = decode('bad data')
    foo['stuff'] = 5
    bar = decode('also bad')
    bar['meep'] = 1
    print('Foo:', foo)
    print('Bar:', bar)

    try:
        assert foo is bar
    except Exception as e:
        print(e)
