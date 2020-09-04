"""
@author: magician
@file:   request_context.py
@date:   2020/9/4
"""
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    """
    hello
    @return:
    """
    print('during view')
    return 'Hello, World!'


@app.teardown_request
def show_teardown(exception):
    """
    show_teardown
    @param exception:
    @return:
    """
    print('after with block')


with app.test_request_context():
    print('during with block')


if __name__ == '__main__':
    with app.test_client() as client:
        client.get('/')
        # the contexts are not popped even though the request ended
        print(request.path)
