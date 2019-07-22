"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/22
"""
import asyncio
import multiprocessing

import aiohttp
import time

from python_core.decorator_demo import log_execution_time


async def download_one(url):
    """
    download_one
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print('Read {} from {}'.format(resp.content_length, url))


async def download_all(sites):
    """
    download_all
    :param sites:
    :return:
    """
    # python3.5
    tasks = [asyncio.ensure_future(download_one(site)) for site in sites]
    # python3.7+
    # tasks = [asyncio.create_task(download_one(site)) for site in sites]

    await asyncio.gather(*tasks)


def main():
    sites = [
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
        'https://www.baidu.com',
        'https://hao.360.cn/',
        'https://www.sogou.com',
    ]
    start_time = time.perf_counter()

    # python3.5
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(download_all(sites))
    finally:
        loop.close()
    # python3.7+
    # asyncio.run(download_all(sites))

    end_time = time.perf_counter()
    print('Download {} sites in {} seconds'.format(len(sites), end_time - start_time))


def cpu_bound(number):
    """
    cpu_bound
    :param number:
    :return:
    """
    print(sum(i * i for i in range(number)))


def calculate_sums(numbers):
    """
    calculate_sums
    :param numbers:
    :return:
    """
    for number in numbers:
        cpu_bound(number)


@log_execution_time
def calculate():
    """
    calculate
    :return:
    """
    numbers = [10000000 + x for x in range(20)]
    calculate_sums(numbers)


def cpu_bound1(number):
    """
    cpu_bound1
    :param number:
    :return:
    """
    return sum(i * i for i in range(number))


def find_sums(numbers):
    """
    find_sums
    :param numbers:
    :return:
    """
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound1, numbers)


@log_execution_time
def calculate1():
    """
    calculate1
    :return:
    """
    numbers = [10000000 + x for x in range(20)]
    find_sums(numbers)


if __name__ == '__main__':
    # main()

    # calculate()

    calculate1()
