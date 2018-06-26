# coding=utf-8

"""
@author: conan
@date: 2018/6/25
"""

if __name__ == '__main__':
    str1 = 'i love you!'
    print(str1.capitalize())

    str2 = 'CHINA'
    print(str2.casefold())
    print(str2.center(40))
    print(str2.count('C'))
    print(str2.endswith('a'))
    print(str2.endswith('A'))

    str3 = 'I\tlove\tyou!'
    print(str3.expandtabs(1))
    print(str3.find('y'))
    print(str3.find('x'))

    str4 = '我爱你'
    print(str4.islower())

    str5 = 'China'
    print(str5.istitle())
    print(str5.join('**'))

    str6 = '      I love you!'
    print(str6.lstrip())

    str7 = 'I love you!'
    print(str7.partition('love'))
    print(str7.replace('you', 'everyone'))
    print(str7.split())

    str8 = '     *****I love you*****       '
    print(str8.strip())
    print(str8.strip().strip('*'))

    str9 = 'Everyone'
    print(str9.swapcase())

    str10 = 'xxxxxxaaaxxxxxxx'
    print(str10.translate(str.maketrans('x', 'b')))

    print('{0} love {1}!'.format('I', 'you'))
    print('{a} love {b}!'.format(a='I', b='you'))
    print('{{0}}'.format('****'))
    print('{0:.1f}{1}'.format(27.658, 'GB'))

    print('%c %c %c' % (97, 98, 99))
    print('%s' % 'I love you!')
    print('%d + %d = %d' % (1, 1, 1+1))
    print('%o' % 10)
    print('%x' % 10)
    print('%X' % 10)
    print('%f' % 27.658)
    print('%e' % 27.658)
    print('%E' % 27.658)
    print('%g' % 27.658)

    print('%5.1f' % 27.658)
    print('%.2e' % 27.658)
    print('%10d' % 5)
    print('%-10d' % 5)
    print('%+d' % -5)
    print('%#o' % 10)
    print('%#X' % 108)
    print('%010d' % 5)
    print('%-010d' % 5)
