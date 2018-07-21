# coding=utf-8

"""
@author: conan
@date: 2018/7/21
"""
import random
import urllib.request
import urllib.parse


def proxy():
    """
    代理
    :return:
    """
    while True:
        url = 'https://www.sojson.com/ip/'
        ip_list = ['101.236.23.202:8866', '118.190.95.43:9001', '125.120.202.201:808']
        proxy_support = urllib.request.ProxyHandler({'http': random.choice(ip_list)})
        opener = urllib.request.build_opener(proxy_support)
        user_agent = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/67.0.3396.87 Safari/537.36')
        opener.add_handlers = [user_agent]
        urllib.request.install_opener(opener)
        response = urllib.request.urlopen(url)
        if response.code == 200:
            html = response.read()
            print(html.decode('utf-8'))
            break


if __name__ == '__main__':
    proxy()
