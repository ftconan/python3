"""
    @author: magician
    @date: 2019/11/15
    @file: comma_demo.py
"""


def yell(text):
    """
    yell
    :param text:
    :return:
    """
    up_text = text.upper() + '!'
    print(up_text)

    return up_text


def greet(func, is_print=1):
    """
    greet
    :param func:     function
    :param is_print: 是否打印： 1: 打印 0： 不打印
    :return:
    """
    greeting = func('Hi, I am a Python program')
    if is_print:
        print(greeting)

    return True


def whisper(text):
    """
    whisper
    :param text:
    :return:
    """
    return text.lower() + '...'


def speak(text):
    """
    speak
    :param text:
    :return:
    """

    def whisper(t):
        return t.lower() + '...'

    return whisper(text)


def get_speak_func(volume):
    """
    get_speak_func
    :param volume:
    :return:
    """
    def whisper(text):
        return text.lower() + '...'

    def yell(text):
        return text.upper() + '!'

    if volume > 0.5:
        return yell
    else:
        return whisper


def get_speak_func1(text, volume):
    """
    get_speak_func1
    :param text:
    :param volume:
    :return:
    """
    def whisper():
        return text.lower() + '...'

    def yell():
        return text.upper() + '!'

    if volume > 0.5:
        return yell
    else:
        return whisper


def make_adder(n):
    """
    make_adder
    :param n:
    :return:
    """
    def add(x):
        return x + n

    return add


class Adder:
    """
    Adder
    """
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return self.n + x


if __name__ == '__main__':
    yell('hello')

    # function variable
    bark = yell
    bark('woof')

    # del function
    try:
        del yell
        yell('hello')
    except Exception as e:
        print(e)
        bark('hey')

    print(bark.__name__)

    # Functions Can Be Stored in Data Structure
    funcs = [bark, str.lower, str.capitalize]
    print(funcs)
    for f in funcs:
        print(f, f('hey there'))
    funcs[0]('heyho')

    # Functions Can Be Passed to Other Function
    greet(bark, is_print=0)
    greet(whisper)
    print(list(map(bark, ['hello', 'hey', 'h1'])))

    # Functions Can Be Nest
    print(speak('Hello World'))

    try:
        whisper('Yo')
        print(speak.whisper)
    except Exception as e:
        print(e)

    print(get_speak_func(0.3))
    print(get_speak_func(0.7))

    speak_func = get_speak_func(0.7)
    print(speak_func('Hello'))

    # Functions Can Capture Local Sta
    print(get_speak_func1('Hello World', 0.7)())
    plus_3 = make_adder(3)
    plus_5 = make_adder(5)
    print(plus_3(4))
    print(plus_5(4))

    # Objects Can Behave Like Function
    adder_3 = Adder(3)
    print(adder_3(4))

    print(callable(adder_3))
    try:
        print(callable(yell))
    except Exception as e:
        print(e)
    print(callable('hello'))
