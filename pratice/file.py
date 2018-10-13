# coding=utf-8

"""
@author: conan
@date: 2018/7/1
"""

if __name__ == '__main__':
    f = open('README.md', encoding='utf-8')
    print(f)

    # print(f.read())
    print(f.read(5))

    print(f.tell())

    f.seek(45, 0)
    print(f.readline())
    print(list(f))

    f.seek(0, 0)
    for each_line in f:
        print(each_line)

    file = open('test.txt', 'w')
    file.write('I love you!')
