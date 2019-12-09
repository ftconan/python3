"""
    @author: magician
    @date: 2019/12/9
    @file: modules_demo.py
"""
import datetime

if __name__ == '__main__':
    print(dir(datetime))
    print(dir(datetime.date))
    print([_ for _ in dir(datetime) if 'date' in _.lower()])
    print(help(datetime))
    print(help(datetime.date))
    print(help(datetime.date.fromtimestamp))
    print(help(dir))
