import sqlite3
from flask import g
import config

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            config.DATABASE_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close the database connection at the end of a request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database using schema.sql."""
    db = get_db()
    with open("schema.sql", "rb") as f:
        db.executescript(f.read().decode("utf8"))
