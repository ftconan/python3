"""
@author: magician
@file:   context_demo.py
@date:   2021/12/12
"""
from fluent_python.context_manager.mirror import LookingGlass
from fluent_python.context_manager.mirror_gen import looking_glass

if __name__ == '__main__':
    with LookingGlass() as what:
        print('Alice, Kitty and Snowdrop')
        print(what)

    # context class
    manager = LookingGlass()
    monster = manager.__enter__()
    print(monster == 'JABBERWOCKY')
    manager.__exit__(None, None, None)
    print(monster)

    # context decorator
    with looking_glass() as what:
        print('Alice, Kitty and Snowdrop')
        print(what)
