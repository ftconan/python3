# coding=utf-8

"""
@author: magician
@date: 2018/9/11
"""
from flaskr import create_app


def test_config():
    """
    test config
    :return:
    """
    assert  not create_app().testing
    assert  create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello World!'
