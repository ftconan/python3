# coding=utf-8

"""
@author: conan
@date: 2018/7/21
"""
import json
import random
import time
import urllib.request
import urllib.parse
import hashlib


def translate():
    """
    有道翻译
    :return:
    """
    while True:
        content = input('请输入需要翻译的内容(输入q!退出): ')
        if content == 'q!':
            break
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&sessionFrom=https://www.google.com/'
        data = dict()
        data['i'] = content
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = str(int(time.time()*1000) + random.randint(1,10))
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_CLICKBUTTION'
        data['typoResult'] = 'false'
        sign = data['client'] + data['i'] + data['salt'] + 'rY0D^0\'nM0}g5Mm1z%1G4'
        data['sign'] = hashlib.md5(sign.encode('utf-8')).hexdigest()
        data = urllib.parse.urlencode(data).encode('utf-8')

        translate_request = urllib.request.Request(url, data)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/67.0.3396.87 Safari/537.36'
        translate_request.add_header('User-Agent', user_agent)
        translate_response = urllib.request.urlopen(url, data)
        translate_result = translate_response.read().decode('utf-8')
        try:
            target = json.loads(translate_result)
            print('{0} 翻译结果: {1}'.format(content, target['translateResult'][0][0]['tgt']))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    translate()
