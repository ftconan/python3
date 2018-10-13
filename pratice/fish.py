# coding=utf-8

"""
@author: conan
@date: 2018/7/14
"""
import random


class Fish:
    """
    Fish
    """
    def __init__(self):
        self.name = 'fish'
        self.x = random.randint(0, 10)
        self.y = random.randint(0, 10)

    def move(self):
        self.x -= 1
        print('{0}的位置: {1},{2}'.format(self.name, self.x, self.y))


class GoldFish(Fish):
    """GoldFish"""
    def __init__(self):
        super().__init__()
        self.name = 'gold_fish'


class Carp(Fish):
    """Carp"""
    def __init__(self):
        super().__init__()
        self.name = 'carp'


class Salmon(Fish):
    """Salmon"""
    def __init__(self):
        super().__init__()
        self.name = 'salmon'


class Shark(Fish):
    """Shark"""
    def __init__(self):
        # Fish.__init__(self)
        super().__init__()
        self.name = 'shark'
        self.hungry = True

    def eat(self):
        if self.hungry:
            print('吃货的梦想就是天天有的吃!')
            self.hungry = False
        else:
            print('太撑了，吃不下了')


if __name__ == '__main__':
    fish = Fish()
    fish.move()

    carp = Carp()
    carp.move()

    goldfish = GoldFish()
    goldfish.move()

    salmon = Salmon()
    salmon.move()

    shark = Shark()
    shark.move()
    shark.eat()
    shark.eat()
