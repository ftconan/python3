"""
@author: magician
@file:   __init__.py.py
@date:   2020/9/7
"""
from flask import Flask

from flask_tutorial.flask_sqlite3.flask_sqlite3 import SQLite3

app = Flask(__name__)
app.config.from_pyfile('the-config.cfg')
db = SQLite3(app)


@app.route('/')
def show_all():
    """
    show_all
    @return:
    """
    # cur = db.connection.cursor()
    # cur.execute('SELECT 1=1')

    with app.app_context():
        cur = db.connection.cursor()
        cur.execute('SELECT 1=1')
