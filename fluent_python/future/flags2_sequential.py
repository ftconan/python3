"""
@author: magician
@file:   flags2_sequential.py
@date:   2021/12/14
"""
import collections
from collections import namedtuple
from concurrent import futures
from http import HTTPStatus

import requests
import tqdm

from fluent_python.future.flags import save_flag

BASE_URL = 'http://flupy.org/data/flags'
Result = namedtuple('Result', 'status cc')


def get_flags(base_url, cc):
    """

    @param base_url:
    @param cc:
    @return:
    """
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    resp = requests.get(url)
    if resp.status_code != 200:
        resp.raise_for_status()

    return resp.content


def download_one(cc, base_url, verbose=False):
    """

    @param cc:
    @param base_url:
    @param verbose:
    @return:
    """
    try:
        image = get_flags(cc, base_url)
    except requests.exceptions.HTTPError as e:
        res = e.response
        if res.status_code == 404:
            status = HTTPStatus.NOT_FOUND
            msg = 'not found'
        else:
            raise
    else:
        save_flag(image, cc.lower() + '.gif')
        status = HTTPStatus.OK
        msg = 'OK'

    if verbose:
        print(cc, msg)

    return Result(status, cc)


def download_many(cc_list, base_url, verbose, max_req):
    """

    @param cc_list:
    @param base_url:
    @param verbose:
    @param max_req:
    @return:
    """
    counter = collections.Counter()
    cc_iter = sorted(cc_list)
    if not verbose:
        cc_iter = tqdm.tqdm(cc_iter)

    status = HTTPStatus.OK
    for cc in cc_iter:
        try:
            res = download_one(cc, base_url, verbose)
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
