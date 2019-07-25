"""
@file: unit_demo.py
@author: magician
@date: 2019/7/25
"""
import unittest
from unittest.mock import MagicMock


def sort(arr):
    """
    sort
    :param arr:
    :return:
    """
    l = len(arr)
    for i in range(0, l):
        for j in range(i+1, l):
            if arr[i] >= arr[j]:
                tmp = arr[i]
                arr[i] = arr[j]
                arr[j] = tmp


class TestSort(unittest.TestCase):
    """
    TestSort
    """
    def test_sort(self):
        arr = [3, 4, 1, 5, 6]
        sort(arr)
        self.assertEqual(arr, [1, 3, 4, 5, 6])


class A(unittest.TestCase):
    """
    A
    """
    def m1(self):
        """
        m1
        :return:
        """
        val = self.m2()
        self.m3(val)

    def m2(self):
        return True

    def m3(self):
        return True

    def test_m1(self):
        """
        test_m1
        :return:
        """
        a = A()
        a.m2 = MagicMock(return_value='custom_val')
        a.m3 = MagicMock()
        a.m1()
        self.assertTrue(a.m2.called)
        a.m3.assert_called_with("custom_val")


if __name__ == '__main__':
    # unittest.main(argv=['first-arg-is-ignored'], exit=False)

    unittest.main()

