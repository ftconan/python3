"""
@author: magician
@file:   flags2_threadpool.py
@date:   2021/12/14
"""
import collections
import time
from concurrent import futures
from http import HTTPStatus

import requests
import tqdm

from fluent_python.future.flags2_sequential import download_one

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEFAULT_CONCUR_REQ = 30
MAX_CONCUR_REQ = 1000


def download_many(cc_list, base_url, verbose, concur_req):
    """

    @param cc_list:
    @param base_url:
    @param verbose:
    @param concur_req:
    @return:
    """
    counter = collections.Counter()
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do_map = {}

        status = HTTPStatus.OK
        for cc in cc_list:
            future = executor.submit(download_one, cc, base_url, verbose)
            to_do_map[future] = cc
        done_iter = futures.as_completed(to_do_map)
        if not verbose:
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))

        for future in done_iter:
            try:
                res = future.result()
                status = HTTPStatus.OK
            except requests.exceptions.HTTPError as e:
                error_msg = 'HTTP error {res.status_code} - {res.reason}'
                error_msg = error_msg.format(res=e.response)
            except requests.exceptions.ConnectionError as e:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status

            if error_msg:
                status = HTTPStatus.INTERNAL_SERVER_ERROR
            counter[status] += 1
            if verbose and error_msg:
                print('*** Error for {}: {}'.format(cc, error_msg))

    return counter


def main(download_many, concur_req, max_req):
    """

    @param download_many:
    @param concur_req:
    @param max_req:
    @return:
    """
    t0 = time.time()
    count = download_many(POP20_CC, BASE_URL, True, 3)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
