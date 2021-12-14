"""
@author: magician
@file:   flags_threadpool_ac.py
@date:   2021/12/14
"""
from concurrent import futures

from fluent_python.future.flags import get_flags, show, save_flag, main

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
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))

        results = []
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)

    return len(list(res))


if __name__ == '__main__':
    main(download_many)
