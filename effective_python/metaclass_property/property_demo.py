"""
@author: magician
@file:   property_demo.py
@date:   2020/1/14
"""
from datetime import timedelta, datetime


class Bucket(object):
    """
    Bucket
    """
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        # self.quota = 0
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        # return 'Bucket(quota=%d)' % self.quota
        return ('Bucket(max_quota=%d, quota_consumed=%d)' %
                (self.max_quota, self.quota_consumed))

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta


def fill(bucket, amount):
    """
    fill
    @param bucket:
    @param amount:
    @return:
    """
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount


def deduct(bucket, amount):
    """
    deduct
    @param bucket:
    @param amount:
    @return:
    """
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount

    return True


if __name__ == '__main__':
    # bucket = Bucket(60)
    # fill(bucket, 100)
    # print(bucket)
    # if deduct(bucket, 99):
    #     print('Had 99 quota')
    # else:
    #     print('Not enough for 99 quota')
    # print(bucket)
    #
    # if deduct(bucket, 3):
    #     print('Had 3 quota')
    # else:
    #     print('Not enough for 3 quota')
    # print(bucket)

    bucket = Bucket(60)
    print('Initial', bucket)
    fill(bucket, 100)
    print('Filled', bucket)

    if deduct(bucket, 99):
        print('Had 99 quota')
    else:
        print('Not enough for 99 quota')
    print('Now', bucket)

    if deduct(bucket, 3):
        print('Had 3 quota')
    else:
        print('Not enough for 3 quota')
    print('Still', bucket)
