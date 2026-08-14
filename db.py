import sqlite3
import os
from flask import g

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    app.teardown_appcontext(close_db)
    with sqlite3.connect(DATABASE_PATH) as conn:
        with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), mode='r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = sqlite3.connect(DATABASE_PATH)
    cur = conn.execute(query, args)
    conn.commit()
    last_id = cur.lastrowid
    cur.close()
    conn.close()
    return last_id
