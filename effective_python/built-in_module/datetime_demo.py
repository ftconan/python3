"""
@author: magician
@file:   datetime_demo.py
@date:   2020/8/11
"""
import time

from datetime import datetime, timezone

import pytz

if __name__ == '__main__':
    # time
    now = 1407694710
    local_tuple = time.localtime(now)
    time_format = '%Y-%m-%d %H:%M:%S'
    time_str = time.strftime(time_format, local_tuple)
    print(time_str)

    time_tuple = time.strptime(time_str, time_format)
    utc_now = time.mktime(time_tuple)
    print(utc_now)

    # parse_format = '%Y-%m-%d %H:%M:%S %Z'
    # depart_sfo = '2014-05-01 15:45:16 PDT'
    # time_tuple = time.strptime(depart_sfo, parse_format)
    # time_str = time.strftime(time_format, time_tuple)
    # print(time_str)

    # arrival_nyc = '2014-05-01 23:33:24 EDT'
    # time_tuple = time.strptime(arrival_nyc, time_format)

    # datetime
    now = datetime(2014, 8, 10, 18, 18, 30)
    now_utc = now.replace(tzinfo=timezone.utc)
    now_local = now_utc.astimezone()
    print(now_local)

    time_str = '2014-08-10 11:18:30'
    now = datetime.strptime(time_str, time_format)
    time_tuple = now.timetuple()
    utc_now = time.mktime(time_tuple)
    print(utc_now)

    arrival_nyc = '2014-05-01 23:33:24'
    nyc_dt_naive = datetime.strptime(arrival_nyc, time_format)
    eastern = pytz.timezone('US/Eastern')
    nyc_dt = eastern.localize(nyc_dt_naive)
    utc_dt = pytz.utc.normalize(nyc_dt.astimezone(pytz.utc))
    print(utc_dt)

    pacific = pytz.timezone('US/Pacific')
    sf_dt = pacific.normalize(utc_dt.astimezone(pacific))
    print(sf_dt)

    nepal = pytz.timezone('Asia/Katmandu')
    nepal_dt = nepal.normalize(utc_dt.astimezone(nepal))
    print(nepal_dt)
