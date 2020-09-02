"""
@author: magician
@file:   test_flaskr.py
@date:   2020/9/2
"""
import json
import os
import tempfile
from contextlib import contextmanager

import click
import flask
import pytest
from flask import Response, g, appcontext_pushed, jsonify, request

from flask_tutorial import flaskr


@pytest.fixture
def client():
    """
    client
    @return:
    """
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])


def test_empty_db(client):
    """
    Start with a blank database.
    @param client:
    @return:
    """
    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def login(client, username, password):
    """
    login
    @param client:
    @param username:
    @param password:
    @return:
    """
    return client.post('/login', data=dict(
        username=username,
        password=password,
    ), follow_redirects=True)


def logout(client):
    """
    logout
    @param client:
    @return:
    """
    return client.get('/logout', follow_redirects=True)


def test_login_logout(client):
    """
    test_login_logout
    @param client:
    @return:
    """
    rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'] + 'x', flaskr.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data

    rv = login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


def test_messages(client):
    """
    Test that messages work.
    @param client:
    @return:
    """
    login(client, flaskr.app.config['USERNAME'], flaskr.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data


app = flask.Flask(__name__)

with app.test_request_context('/?name=Peter'):
    assert flask.request.path == '/'
    assert flask.request.args['name'] == 'Peter'

    app.preprocess_request()

    resp = Response('...')
    resp = app.process_response(resp)


def fetch_current_user_from_database():
    return ''


def get_user():
    """
    get_user
    @return:
    """
    user = getattr(g, 'user', None)
    if user is None:
        user = fetch_current_user_from_database()
        g.user = user

    return user


@contextmanager
def user_set(app, user):
    """
    user_set
    @param app:
    @param user:
    @return:
    """

    def handler(sender, **kwargs):
        g.user = user

    with appcontext_pushed.connected_to(handler, app):
        yield


@app.route('/users/me')
def user_me():
    """
    user_me
    @return:
    """
    return jsonify(username=g.user.username)


my_user = None

with user_set(app, my_user):
    with app.test_client() as c:
        resp = c.get('/users/me')
        data = json.loads(resp.data)
        app.assert_equal(data['username'], my_user.username)

with app.test_client() as c:
    rv = c.get('/?tequila=42')
    assert request.args['tequila'] == '42'

with app.test_client() as c:
    rv = c.get('/')
    assert flask.session['foo'] == 42

with app.test_client() as c:
    with c.session_transaction() as sess:
        sess['a_key'] = 'a value'

    # once this is reached the session was stored and ready to be used by the client
    c.get(...)


def generate_token(email, password):
    pass


@app.route('/api/auth')
def auth():
    json_data = request.get_json()
    email = json_data['email']
    password = json_data['password']
    return jsonify(token=generate_token(email, password))


email = ''


def verify_token(email, param):
    pass


with app.test_client() as c:
    rv = c.post('/api/auth', json={
        'email': 'flask@example.com', 'password': 'secret'
    })
    json_data = rv.get_json()
    assert verify_token(email, json_data['token'])


@app.cli.command('hello')
@click.option('--name', default='World')
def hello_command(name):
    click.echo(f'Hello, {name}!')


def test_hello():
    runner = app.test_cli_runner()

    # invoke the command directly
    result = runner.invoke(hello_command, ['--name', 'Flask'])
    assert 'Hello, Flask' in result.output

    # or by name
    result = runner.invoke(args=['hello'])
    assert 'World' in result.output


def upper(ctx, param, value):
    if value is not None:
        return value.upper()


@app.cli.command('hello')
@click.option('--name', default='World', callback=upper)
def hello_command(name):
    click.echo(f'Hello, {name}!')


def test_hello_params():
    context = hello_command.make_context('hello', ['--name', 'flask'])
    assert context.params['name'] == 'FLASK'
