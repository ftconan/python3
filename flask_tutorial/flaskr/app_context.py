"""
@author: magician
@file:   app_context.py
@date:   2020/9/3
"""
from flask import Flask, g
from werkzeug.local import LocalProxy

from flask_tutorial.flask_demo.hello_flask import app
from flask_tutorial.flaskr.db import init_db


def create_app():
    """
    create_app
    @return:
    """
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app


def connect_to_database():
    """
    connect_to_database
    @return:
    """
    return ''


def get_db():
    """
    get_db
    @return:
    """
    if 'db' not in g:
        g.db = connect_to_database()

    return g.db


@app.teardown_appcontext
def teardown_db():
    """
    teardown_db
    @return:
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


db = LocalProxy(get_db)
