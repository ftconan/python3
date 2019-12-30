"""
    @author: magician
    @date: 2019/12/30
    @file: mixin_demo.py
"""
import json


class ToDictMixin(object):
    """
    ToDictMixin
    """
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)

        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value


class BinaryTree(ToDictMixin):
    """
    BinaryTree
    """
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BinaryTreeWithParent(BinaryTree):
    """
    BinaryTreeWithParent
    """
    def __init__(self, value, left=None, right=None, parent=None):
        super().__init__(value, left=left, right=right)
        self.parent = parent

    def _traverse(self, key, value):
        if isinstance(value, BinaryTreeWithParent) and key == 'parent':
            return value.value
        else:
            return super()._traverse(key, value)


class NamedSubTree(ToDictMixin):
    """
    NamedSubTree
    """
    def __init__(self, name, tree_with_parent):
        self.name = name
        self.tree_with_parent = tree_with_parent


class JsonMixin(object):
    """
    JsonMixin
    """
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)

        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())


class DatacenterRack(ToDictMixin, JsonMixin):
    """
    DatacenterRack
    """
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]


class Switch(ToDictMixin, JsonMixin):
    """
    Switch
    """
    def __init__(self, **kwargs):
        # super(JsonMixin, self).__init__(**kwargs)
        pass


class Machine(ToDictMixin, JsonMixin):
    """
    Switch
    """
    def __init__(self, **kwargs):
        # super(JsonMixin, self).__init__(**kwargs)
        pass


if __name__ == '__main__':
    tree = BinaryTree(10,
                      left=BinaryTree(7, right=BinaryTree(9)),
                      right=BinaryTree(13, right=BinaryTree(11)))
    print(tree.to_dict())

    root = BinaryTreeWithParent(10)
    root.left = BinaryTreeWithParent(7, parent=root)
    root.left.right = BinaryTreeWithParent(9, parent=root.left)
    print(root.to_dict())

    my_tree = NamedSubTree('foobar', root.left.right)
    print(my_tree.to_dict())

    serialized = """{
        "switch": {"port": 5, "speed": 1e9},
        "machines": [
            {"core": 8, "ram": 32e9, "disk": 5e12},
            {"core": 4, "ram": 16e9, "disk": 1e12},
            {"core": 2, "ram": 4e9, "disk": 500e9}
        ]
    }"""
    deserialized = DatacenterRack.from_json(serialized)
    roundtrip = deserialized.to_json()
    assert json.loads(serialized) == json.loads(roundtrip)
