"""
@author: magician
@file:   flags.py
@date:   2021/12/14
"""
import os
import sys
import time

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = os.path.join(os.path.dirname(__file__), 'downloads/')


def save_flag(img, filename):
    """

    @param img:
    @param filename:
    @return:
    """
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


def get_flags(cc):
    """

    @param cc:
    @return:
    """
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)

    return resp.content


def show(text):
    """

    @param text:
    @return:
    """
    print(text, end=' ')
    sys.stdout.flush()


def download_many(cc_list):
    """

    @param cc_list:
    @return:
    """
    for cc in sorted(cc_list):
        image = get_flags(cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')

    return len(cc_list)


def main(download_many):
    """

    @param download_many:
    @return:
    """
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many)
