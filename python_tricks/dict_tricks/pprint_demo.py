"""
    @author: magician
    @date: 2019/12/9
    @file: pprint_demo.py
"""
import json
import pprint

if __name__ == '__main__':
    mapping = {'a': 23, 'b': 42, 'c': 0xc0ffee}
    print(str(mapping))
    print(json.dumps(mapping, indent=4, sort_keys=True))

    try:
        print(json.dumps({all: 'yup'}))
    except Exception as e:
        print(e)

    mapping['d'] = {1, 2, 3}
    try:
        print(json.dumps(mapping))
    except Exception as e:
        print(e)

    pprint.pprint(mapping)
