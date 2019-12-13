"""
    @author: magician
    @date: 2019/12/13
    @file: try_demo.py
"""
import json


UNDEFINED = object()


def load_json_key(data, key):
    """
    load_json_key
    :param data:
    :param key:
    :return:
    """
    try:
        result_dict = json.loads(data)
    except Exception as e:
        raise KeyError from e
    else:
        return result_dict[key]


def divide_json(path):
    """
    divide_json
    :param path:
    :return:
    """
    handle = open(path, 'r+')
    try:
        data = handle.read()
        op = json.loads(data)
        value = (op['numerator'] / op['denominator'])
    except ZeroDivisionError as e:
        return UNDEFINED
    else:
        op['result'] = value
        result = json.dumps(op)
        handle.seek(0)
        handle.write(result)
        return value
    finally:
        handle.close()


if __name__ == '__main__':
    handle = open('/home/magician/Project/python3/data/test.txt')
    try:
        data = handle.read()
    finally:
        handle.close()
