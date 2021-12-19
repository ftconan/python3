"""
@author: magician
@file:   counter_test.py
@date:   2021/12/19
"""


def partition(arr, begin, end):
    pivot = end
    counter = begin

    for i in range(begin, end):
        if arr[i] < arr[pivot]:
            arr[counter], arr[i] = arr[i], arr[counter]
            counter += 1

    arr[counter], arr[pivot] = arr[pivot], arr[counter]

    return counter


def quick_sort(arr, begin, end):
    if end <= begin:
        return
    
    pivot = partition(arr, begin, end)
    quick_sort(arr, begin, pivot-1)
    quick_sort(arr, pivot+1, end)


def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            break
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result


if __name__ == '__main__':
    array = [10, 7, 8, 9, 1, 5]
    quick_sort(array, 0, len(array)-1)
    print(array)

    binary_arr = [2, 3, 4, 10, 40]
    print(binary_search(binary_arr, 10))
