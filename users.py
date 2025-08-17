import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

def create_user(username, password):
    """Insert a new user with a hashed password."""
    db = get_db()
    try:
        db.execute(
            "INSERT INTO user (username, password_hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        db.commit()
    except sqlite3.IntegrityError:
        # raised if username is already taken
        raise

def check_login(username, password):
    """Return user_id if credentials are valid, else None."""
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?",
        (username,)
    ).fetchone()
    if user and check_password_hash(user["password_hash"], password):
        return user["id"]
    return None

def get_user(user_id):
    """Fetch basic user info by id."""
    return get_db().execute(
        "SELECT id, username FROM user WHERE id = ?",
        (user_id,)
    ).fetchone()

def get_announcements(user_id):
    """All announcements created by a given user."""
    return get_db().execute(
        "SELECT * FROM announcement WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

def get_announcement_count(user_id):
    """How many announcements this user has created."""
    row = get_db().execute(
        "SELECT COUNT(*) AS c FROM announcement WHERE user_id = ?",
        (user_id,)
    ).fetchone()
    return row["c"] if row else 0
