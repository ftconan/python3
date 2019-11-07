"""
@file: qt_crawler.py
@author: magician
@date: 2019/8/12
"""
import copy
import json
import ssl
import time
import _thread
import requests
import websocket


count = 5


def get_orderbook():
    """
    get orderbook
    :return:
    """
    orderbook = requests.get('https://api.gemini.com/v1/book/btcusd').json()
    return orderbook


# def on_message(ws, message):
#     """
#     on message
#     :param ws:      websocket
#     :param message:
#     :return:
#     """
#     print('Received: ' + message)


def on_message(ws, message):
    """
    on message
    :param ws:      websocket
    :param message:
    :return:
    """
    global count
    print(message)
    count -= 1
    # close websocket
    if count == 0:
        ws.close()


def on_open(ws):
    """
    on open
    :param ws:
    :return:
    """
    def gao():
        for i in range(5):
            time.sleep(0.01)
            msg = "{0}".format(0.01)
            ws.send(msg)
            print('Sent: ' + msg)
        time.sleep(1)

        # close websocket
        ws.close()
        print('Websocket closed')

    _thread.start_new_thread(gao, ())


class OrderBook(object):
    """
    OrderBook
    """
    BIDS = 'bid'
    ASKS = 'ask'

    def __init__(self, limit=20):
        """
        init
        :param limit:
        """
        self.limit = limit
        # (price, amount)
        self.bids = {}
        self.asks = {}

        self.bids_sorted = {}
        self.asks_sorted = {}

    def insert(self, price, amount, direction):
        """
        insert
        :param price:
        :param amount:
        :param direction:
        :return:
        """
        if direction == self.BIDS:
            if amount == 0:
                if price in self.bids:
                    del self.bids[price]
            else:
                self.bids[price] = amount
        elif direction == self.ASKS:
            if amount == 0:
                if price in self.asks:
                    del self.asks[price]
            else:
                self.asks[price] = amount
        else:
            print('WARNING: unknown direction {}'.format(direction))

    def sort_and_truncate(self):
        """
        sort and truncate
        :return:
        """
        # sort
        self.bids_sorted = sorted([(price, amount) for price, amount in self.bids.items()], reverse=True)
        self.asks_sorted = sorted([(price, amount) for price, amount in self.asks.items()])

        # truncate
        self.bids_sorted = self.bids_sorted[:self.limit]
        self.asks_sorted = self.asks_sorted[:self.limit]

        # copy back to bids and asks
        self.bids = dict(self.bids_sorted)
        self.asks = dict(self.asks_sorted)

    def get_copy_of_bids_and_asks(self):
        """
        get copy of bids and asks
        :return:
        """
        return copy.deepcopy(self.bids_sorted), copy.deepcopy(self.asks_sorted)


class Crawler:
    """
    Crawler
    """
    def __init__(self, symbol, output_file):
        """
        init
        :param symbol:
        :param output_file:
        """
        self.orderbook = OrderBook(limit=10)
        self.output_file = output_file

        self.ws = websocket.WebSocketApp('wss://api.gemini.com/v1/marketdata/{}'.format(symbol),
                                         on_message=lambda ws, message: self.on_message(message))
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})

    def on_message(self, message):
        """
        on_message
        :param message:
        :return:
        """
        data = json.loads(message)
        for event in data['events']:
            price, amount, direction = float(event['price']), float(event['remaining']), event['side']
            self.orderbook.insert(price, amount, direction)

        # orderbook sort, select top orderbook
        self.orderbook.sort_and_truncate()

        # output to file
        with open(self.output_file, 'a+') as f:
            bids, asks = self.orderbook.get_copy_of_bids_and_asks()
            output = {
                'bids': bids,
                'asks': asks,
                'ts': int(time.time() * 1000)
            }
            # print(output)
            f.write(json.dumps(output) + '\n')


if __name__ == '__main__':
    # n = 10
    # latency = timeit.timeit('get_orderbook()', setup='from __main__ import get_orderbook', number=n) * 1.0 / n
    # print('Latency is {} ms'.format(latency * 1000))
    #
    # ws = websocket.WebSocketApp('ws://echo.websocket.org', on_message=on_message, on_open=on_open)
    # ws.run_forever()

    # ws = websocket.WebSocketApp(
    #     "wss://api.gemini.com/v1/marketdata/btcusd?top_of_book=true&offers=true",
    #     on_message=on_message)
    # ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    crawler = Crawler(symbol='BTCUSD', output_file='../data/BTCUSD.txt')
