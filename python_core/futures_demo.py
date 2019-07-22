"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/22
"""
import concurrent.futures
import requests
import time


def download_one(url):
    """
    download_one
    :param url:
    :return:
    """
    resp = requests.get(url)
    print('Read {} from {}'.format(len(resp.content), url))


def download_all(sites):
    """
    download_all
    :param sites:
    :return:
    """
    for site in sites:
        download_one(site)


def download_all1(sites):
    """
    download_all1
    :param sites:
    :return:
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_one, sites)


def download_all2(sites):
    """
    download_all2
    :param sites:
    :return:
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        to_do = []
        for site in sites:
            future = executor.submit(download_one, site)
            to_do.append(future)

        for future in concurrent.futures.as_completed(to_do):
            future.result()


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
    # download_all(sites)
    # download_all1(sites)
    download_all2(sites)
    end_time = time.perf_counter()
    print('Download {} sites in {} seconds'.format(len(sites), end_time - start_time))


if __name__ == '__main__':
    main()
