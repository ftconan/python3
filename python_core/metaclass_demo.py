"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/17
"""
import yaml


class YAMLObjectMetaClass(type):
    """
    YAMLObjectMetaClass
    """
    def __init__(cls, name, bases, kwds):
        super(YAMLObjectMetaClass, cls).__init__(name, bases, kwds)
        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
            cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)


class YAMLObject(metaclass=YAMLObjectMetaClass):
    """
    YAMLObject
    """
    yaml_loader = yaml.Loader


class Monster(yaml.YAMLObject):
    """
    Monster
    """
    yaml_tag = '!Monster'

    def __init__(self, name, hp, ac, attacks):
        """
        init
        :param name:
        :param hp:
        :param ac:
        :param attacks:
        """
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks

    def __repr__(self):
        """
        repr
        :return:
        """
        return '%s(name=%r, hp=%r, ac=%r, attacks=%r)' % (
            self.__class__.__name__, self.name, self.hp, self.ac, self.attacks)


class MyClass:
    """
    MyClass
    """
    data = 1


if __name__ == '__main__':
    # yaml.load(
    #     """
    #     ---!Monster
    #     name:Cave spider
    #     hp:[2,6]
    #     ac:16
    #     attacks:[BITE, HURT]
    #     """
    # )

    monster = Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])
    print(yaml.dump(monster))

    instance = MyClass()
    print(type(instance))
    print(type(MyClass))

    print(MyClass, instance)
    print(instance.data)

    MyClass1 = type('MyClass1', (), {'data': 1})
    instance1 = MyClass1()
    print(MyClass1, instance1)
    print(instance1.data)
