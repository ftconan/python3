# coding=utf-8

"""
@author: conan
@date: 2018/8/26
"""


def factorial(n):
    """
    n阶乘
    :param n:
    :return:
    """
    return 1 if n < 2 else n * factorial(n - 1)


def tag(name, *content, cls=None, **attrs):
    """
    Generate one or more HTML tags
    :param name:       <img>
    :param content:    hello
    :param cls:        class      hello
    :param attrs:      {'src': 'www.google.com'}
    :return:           <img class='hello' src='www.google.com'>hello</img>
    """
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value) for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''

    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


if __name__ == '__main__':
    # generator expression
    print(list(map(factorial, range(6))))
    print(list(map(factorial, filter(lambda a: a % 2, range(6)))))

    # modern replacements for map, filter and reduce
    print([factorial(n) for n in range(6)])
    print([factorial(n) for n in range(6) if n % 2])

    # html tag
    print(tag('br'))
    print(tag('p', 'hello'))
    print(tag('p', 'hello', 'world'))
    print(tag('p', 'hello', id=33))
    print(tag('p', 'hello', 'world', cls='sidebar'))
    print(tag(content='testing', name="img"))
    my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
    print(tag(**my_tag))
