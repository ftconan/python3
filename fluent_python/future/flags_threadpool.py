"""
@author: magician
@file:   flags_threadpool.py
@date:   2021/12/14
"""
from concurrent import futures

from fluent_python.future.flags import get_flags, show, save_flag, main

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
MAX_WORKERS = 20


def download_one(cc):
    """

    @param cc:
    @return:
    """
    image = get_flags(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')

    return cc


def download_many(cc_list):
    """

    @param cc_list:
    @return:
    """
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))

    return len(list(res))


if __name__ == '__main__':
    main(download_many)
