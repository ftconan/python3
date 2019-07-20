"""
@file: decorator_demo.py
@author: magician
@date: 2019/7/20
"""
import asyncio
import random
import time

import aiohttp
import requests
from bs4 import BeautifulSoup

from python_core.decorator_demo import log_execution_time


def crawl_page(url):
    """
    crawl page
    :param url:
    :return:
    """
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    time.sleep(sleep_time)
    print('OK {}'.format(url))


@log_execution_time
def main(urls):
    """
    main
    :param urls:
    :return:
    """
    for url in urls:
        crawl_page(url)


async def crawl_page1(url):
    """
    crawl page1
    :param url:
    :return:
    """
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    await asyncio.sleep(sleep_time)
    print('OK {}'.format(url))


@log_execution_time
async def main1(urls):
    """
    main1
    :param urls:
    :return:
    """
    tasks = [asyncio.create_task(crawl_page1(url)) for url in urls]
    for task in tasks:
        await task


async def crawl_page2(url):
    """
    crawl_page2
    :param url:
    :return:
    """
    print('crawling {}'.format(url))
    sleep_time = int(url.split('_')[-1])
    await asyncio.sleep(sleep_time)
    print('OK {}'.format(url))


@log_execution_time
async def main2(urls):
    """
    main1
    :param urls:
    :return:
    """
    tasks = [asyncio.create_task(crawl_page1(url)) for url in urls]
    await asyncio.gather(*tasks)


async def worker1():
    """
    worker1
    :return:
    """
    print('worker1 start')
    await asyncio.sleep(1)
    print('worker1 done')


async def worker2():
    """
    worker2
    :return:
    """
    print('worker2 start')
    await asyncio.sleep(2)
    print('worker2 done')


async def main3():
    """
    main3
    :return:
    """
    task1 = asyncio.create_task(worker1())
    task2 = asyncio.create_task(worker2())
    print('before wait')
    # await worker1()
    await task1
    print('awaited worker1')
    # await worker2()
    await task2
    print('awaited worker2')


async def worker4():
    """
    worker4
    :return:
    """
    await asyncio.sleep(1)

    return 1


async def worker5():
    """
    worker5
    :return:
    """
    await asyncio.sleep(2)

    return 2 / 0


async def worker6():
    """
    worker6
    :return:
    """
    await asyncio.sleep(3)

    return 3


async def main4():
    """
    main4
    :return:
    """
    task4 = asyncio.create_task(worker4())
    task5 = asyncio.create_task(worker5())
    task6 = asyncio.create_task(worker6())

    await asyncio.sleep(2)
    task6.cancel()

    res = await asyncio.gather(task4, task5, task6, return_exceptions=True)
    print(res)


async def consumer(queue, id):
    """
    consumer
    :param queue:
    :param id:
    :return:
    """
    while True:
        val = await queue.get()
        print('{} get a val: {}'.format(id, val))
        await asyncio.sleep(1)


async def producer(queue, id):
    """
    producer
    :param queue:
    :param id:
    :return:
    """
    for i in range(5):
        val = random.randint(1, 10)
        await queue.put(val)
        print('{} put a val: {}'.format(id, val))
        await asyncio.sleep(1)


async def main5():
    """
    main5
    :return:
    """
    queue = asyncio.Queue()

    consumer1 = asyncio.create_task(consumer(queue, 'consumer1'))
    consumer2 = asyncio.create_task(consumer(queue, 'consumer2'))

    producer1 = asyncio.create_task(producer(queue, 'producer1'))
    producer2 = asyncio.create_task(producer(queue, 'producer2'))

    await asyncio.sleep(10)
    consumer1.cancel()
    consumer2.cancel()

    await asyncio.gather(consumer1, consumer2, producer1, producer2, return_exceptions=True)


def crawl_movies():
    """
    crawl_movies
    :return:
    """
    url = "http://movie.douban.com/cinema/later/beijing"
    init_page = requests.get(url).content
    init_soup = BeautifulSoup(init_page, 'lxml')

    all_movies = init_soup.find('div', id='showing-soon')
    for each_movie in all_movies.find_all('div', class_='item'):
        all_a_tag = each_movie.find_all('a')
        all_li_tag = each_movie.find_all('li')

        movie_name = all_a_tag[1].text
        url_to_fetch = all_a_tag[1]['href']
        movie_date = all_li_tag[0].text

        response_item = requests.get(url_to_fetch).content
        soup_item = BeautifulSoup(response_item, 'lxml')
        img_tag = soup_item.find('img')

        print('{} {} {}'.format(movie_name, movie_date, img_tag['src']))


async def fetch_content(url):
    """
    fetch content
    :param url:
    :return:
    """
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:

            return await response.text()


def crawl_movies1():
    """
    crawl_movies1
    :return:
    """
    url = ["http://movie.douban.com/cinema/later/beijing"]
    init_page = requests.get(url).content
    init_soup = BeautifulSoup(init_page, 'lxml')

    movie_names, urls_to_fetch, movie_dates = [], [], []

    all_movies = init_soup.find('div', id='showing-soon')
    for each_movie in all_movies.find_all('div', class_='item'):
        all_a_tag = each_movie.find_all('a')
        all_li_tag = each_movie.find_all('li')

        movie_names.append(all_a_tag[1].text)
        urls_to_fetch.append(all_a_tag[1]['href'])
        movie_dates.append(all_li_tag[0].text)

    tasks = [fetch_content(url) for url in urls_to_fetch]
    pages = asyncio.gather(*tasks)

    for movie_name, movie_date, page in zip(movie_names, movie_dates, pages):
        soup_item = BeautifulSoup(page, 'lxml')
        img_tag = soup_item.find('img')

        print('{} {} {}'.format(movie_name, movie_date, img_tag['src']))



if __name__ == '__main__':
    # main(['url_1', 'url_2', 'url_3', 'url_4'])

    # python3.7
    asyncio.run(main1(['url_1', 'url_2', 'url_3', 'url_4']))

    asyncio.run(main2(['url_1', 'url_2', 'url_3', 'url_4']))

    asyncio.run(main3())

    asyncio.run(main4())

    asyncio.run(main5())

    crawl_movies()

    crawl_movies1()
