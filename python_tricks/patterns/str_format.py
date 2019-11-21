"""
    @author: magician
    @date: 2019/11/19
    @file: str_format.py
"""
import dis
from string import Template

SECRET = 'this-is-a-secret'


def greet(new_name, question):
    """
    greet
    :param new_name:
    :param question:
    :return:
    """
    # return f"Hello, {name}! How's it {question}?"
    return "Hello, " + new_name + "! How's it " + question + "?"


class Error:
    """
    Error
    """

    def __init__(self):
        pass


if __name__ == '__main__':
    errno = 50159747054
    name = 'Bob'

    # 1.Old Style
    print('Hello, %s' % name)
    print('%x' % errno)
    print('Hey %s, there is a 0x%x error!' % (name, errno))
    print('Hey %(name)s, there is a 0x%(errno)x error!' % {"name": name, "errno": errno})

    # 2.New Style
    print('Hello, {}'.format(name))
    print('Hey {name}, there is a 0x{errno:x} error!'.format(name=name, errno=errno))

    # 3.Literal String Interpolation (Python 3.6)
    # print(f'Hello, {name}')
    # a, b = 5, 10
    # print(f'Five plus ten is {a + b} and not {2 * (a + b)}.')
    # greet('Bob', 'going')
    dis.dis(greet)
    # print(f"Hey {name}, there's a {errno:#x} error!")

    # 4.Template Strings
    t = Template('Hey, $name!')
    t.substitute(name=name)
    templ_string = 'Hey $name, there is a $error error!'
    print(Template(templ_string).substitute(name=name, error=hex(errno)))

    err = Error()
    user_input = '{error.__init__.__globals__[SECRET]}'
    print(user_input.format(error=err))
    # user_input = '${error.__init__.__globals__[SECRET]}'
    # print(Template(user_input).substitute(error=err))
