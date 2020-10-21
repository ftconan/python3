"""
@author: magician
@file:   registration.py
@date:   2020/10/20
"""

registry = []


def register(func):
    """
    register
    @param func:
    @return:
    """
    print('running register(%s)' % func)
    registry.append(func)

    return func


@register
def f1():
    """
    f1
    @return:
    """
    print('running f1()')


@register
def f2():
    """
    f2
    @return:
    """
    print('running f2()')


def f3():
    """
    f3
    @return:
    """
    print('running f3()')


def main():
    """
    main
    @return:
    """
    print('running main')
    print('registry ->', registry)
    f1()
    f2()
    f3()


act_registry = set()


def act_register(active=True):
    """
    act_register
    @param active:
    @return:
    """
    def decorate(func):
        print('running register(active=%s)->decorate(%s)' % (active, func))
        if active:
            act_registry.add(func)
        else:
            act_registry.discard(func)

        return func

    return decorate


@act_register(active=False)
def act_f1():
    """
    act_f1
    @return:
    """
    print('running act_f1()')


@act_register()
def act_f2():
    """
    act_f2
    @return:
    """
    print('running act_f2()')


def act_f3():
    """
    act_f3
    @return:
    """
    print('running act_f3()')


def act_main():
    """
    act_main
    @return:
    """
    print('running act_main')
    print('registry ->', act_registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()

    # act_register
    act_main()
