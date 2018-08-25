# coding=utf-8

"""
@author: conan
@date: 2018/7/9
"""
import pickle

if __name__ == '__main__':
    # pickle 保存数据文二进制
    my_list = ['123', 3434, ['another', 'xx']]
    pickle_file = open('my_list.pkl', 'wb')
    pickle.dump(my_list, pickle_file)
    pickle_file.close()

    # 打开pickle
    pickle_file = open('my_list.pkl', 'rb')
    my_list2 = pickle.load(pickle_file)
    print(my_list2)
