"""
@author: magician
@file:   flask_sqlite3.py
@date:   2020/9/7
"""
import sqlite3

from flask import current_app, _app_ctx_stack


class SQLite3(object):
    """
    SQLite3
    """

    def __init__(self, app=None):
        """
        __init__
        @param app:
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        init_app
        @param app:
        @return:
        """
        app.config.setdefault('SQLITE3_DATABASE', ':memory:')
        app.teardown_appcontext(self.teardown)

    def connect(self):
        return sqlite3.connect(current_app.config['SQLITE3_DATABASE'])

    def teardown(self, exception):
        """
        teardown
        @param exception:
        @return:
        """
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()

    @property
    def connection(self):
        """
        connection
        @return:
        """
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'sqlite3_db'):
                ctx.sqlite3_db = self.connect()

            return ctx.sqlite3_db
