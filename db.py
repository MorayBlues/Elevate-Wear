import os
from flask import g
import psycopg2
def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(os.environ.get("DATABASE_URL"))
        g.db.autocommit = False
    return g.db
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
def init_app(app):
    app.teardown_appcontext(close_db)            