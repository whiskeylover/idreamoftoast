""" config.py """
import os

from flask import Flask
from peewee import MySQLDatabase, SqliteDatabase

#-------------------------------------------------------------------------------
# Environment
#-------------------------------------------------------------------------------
DB       = 'idreamoftoast'
ENV      = os.environ.get('TOAST_PRODUCTION', None)
HOST     = os.environ.get('TOAST_HOST', None)
USER     = os.environ.get('TOAST_USER', None)
PASSWD   = os.environ.get('TOAST_PASSWD', None)
LOG_PATH = os.environ.get('TOAST_LOG_PATH', './')

#-------------------------------------------------------------------------------
# Config Methods
#-------------------------------------------------------------------------------
def get_app():
    app = None
    # If env is set, we are in production!
    if ENV:
        app = Flask(__name__)

        import logging
        file_handler = logging.FileHandler(LOG_PATH + 'flask.log')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        app.logger.addHandler(file_handler)
    else:
        # Development settings here!
        app = Flask(__name__, static_folder='public', static_url_path='')

        @app.route("/")
        def root():
            return app.send_static_file('index.html')

    return app

def get_database():
    db = None
    # If env is set, we are in production!
    if ENV:
        # Production settings here!
        if not (HOST or USER or PASSWD):
            import sys
            print 'Environment variables NOT set!'
            sys.exit()
        db = MySQLDatabase(DB, host=HOST, user=USER, passwd=PASSWD)
    else:
        # Development settings here!
        db = SqliteDatabase('toast.db', threadlocals=True)

    return db
