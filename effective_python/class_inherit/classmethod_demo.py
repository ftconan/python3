"""
    @author: magician
    @date: 2019/12/24
    @file: classmethod_demo.py
"""
import os
from threading import Thread

TEMP_DIR = '/home/magician/Project/python3/data/1.txt'


class InputData(object):
    """
    InputData
    """
    def read(self):
        raise NotImplementedError


class PathInputData(InputData):
    """
    PathInputData
    """
    def __init__(self, path):
        super().__init__()
        self.path = path

    def read(self):
        return open(self.path).read()


class Worker(object):
    """
    Worker
    """
    def __init__(self, input_data):
        self.input_data = input_data
        self.result = None

    def map(self):
        raise NotImplementedError

    def reduce(self, other):
        raise NotImplementedError


class LineCountWorker(Worker):
    """
    LineCountWorker
    """
    def map(self):
        data = self.input_data.read()
        self.result = data.count('\n')

    def reduce(self, other):
        self.result += other.result


def generate_inputs(data_dir):
    """
    generate_inputs
    :param data_dir:
    :return:
    """
    for name in os.listdir(data_dir):
        yield PathInputData(os.path.join(data_dir, name))


def create_workers(input_list):
    """
    create_workers
    :param input_list:
    :return:
    """
    workers = []

    for input_data in input_list:
        workers.append(LineCountWorker(input_data))

    return workers


def execute(workers):
    """
    execute
    :param workers:
    :return:
    """
    threads = [Thread(target=w.map)for w in workers]
    for thread in threads: thread.start()
    for thread in threads: thread.join()

    first, rest = workers[0], workers[1:]
    for worker in workers:
        first.reduce(worker)

    return first.result


def mapreduce(data_dir):
    """
    mapreduce
    :param data_dir:
    :return:
    """
    inputs = generate_inputs(data_dir)
    workers = create_workers(inputs)

    return execute(workers)


def write_test_files(tmpdir):
    """
    write_test_files
    :param tmpdir:
    :return:
    """
    # os.write(['111'])
    pass

    return tmpdir


class GenericInputData(object):
    """
    GenericInputData
    """
    def read(self):
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        raise NotImplementedError


# class PathInputData(GenericInputData):
#     """
#     PathInputData
#     """
#     def read(self):
#         return open(self.path).read()
#
#     @classmethod
#     def generate_inputs(cls, config):
#         data_dir = config['data_dir']
#         for name in os.listdir(data_dir):
#             yield cls(os.path.join(data_dir, name))


# class GenericWorker(object):
#     """
#     GenericWorker
#     """
#     def map(self):
#         raise NotImplementedError
#
#     def reduce(self, other):
#         raise NotImplementedError
#
#     @classmethod
#     def create_workers(cls, input_class, config):
#         workers = []
#
#         for input_data in input_class.generate_inputs(config):
#             workers.append(cls(input_data))
#
#         return workers


# def mapreduce(worker_class, input_class, config):
#     """
#     mapreduce
#     :param worker_class:
#     :param input_class:
#     :param config:
#     :return:
#     """
#     workers = worker_class.create_workers(input_class, config)
#
#     return execute(workers)


if __name__ == '__main__':
    with open(TEMP_DIR) as tmpdir:
        write_test_files(tmpdir)
        result = mapreduce(tmpdir)
    print('There are', result, 'lines')

    # with open(TEMP_DIR) as tmpdir:
    #     write_test_files(tmpdir)
    #     result = mapreduce(LineCountWorker, PathInputData, config)
