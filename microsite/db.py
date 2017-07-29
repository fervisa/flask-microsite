import sqlite3
from os import getcwd
from flask import g, Flask

DATABASE = "{folder}/microsite.db".format(folder=getcwd())

def make_dicts(cursor, row):
    """Convenience method to return dictionaries instead
    of tuples when fetching data from the DB
    """
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    """Get db connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    """Send query to DB and return tuples

    one - Return a single tuple
    """
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
