from db import get_db

def create_announcement(title, description, location, time, slots_needed, user_id):
    db = get_db()
    db.execute(
        """INSERT INTO announcement
           (title, description, location, time, slots_needed, user_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (title, description, location, time, slots_needed, user_id)
    )
    db.commit()

def get_announcements():
    """Return all announcements with their creators’ usernames."""
    return get_db().execute(
        "SELECT a.*, u.username "
        "FROM announcement a JOIN user u ON a.user_id = u.id"
    ).fetchall()

def get_announcement(announcement_id):
    """Fetch a single announcement by id."""
    return get_db().execute(
        "SELECT * FROM announcement WHERE id = ?",
        (announcement_id,)
    ).fetchone()

def update_announcement(announcement_id, title, description, location, time, slots_needed):
    db = get_db()
    db.execute(
        """UPDATE announcement
           SET title = ?, description = ?, location = ?, time = ?, slots_needed = ?
           WHERE id = ?""",
        (title, description, location, time, slots_needed, announcement_id)
    )
    db.commit()

def delete_announcement(announcement_id):
    db = get_db()
    db.execute(
        "DELETE FROM announcement WHERE id = ?",
        (announcement_id,)
    )
    db.commit()

def find_announcements(keyword):
    """Search announcements by title or description."""
    like = f"%{keyword}%"
    return get_db().execute(
        "SELECT a.*, u.username "
        "FROM announcement a JOIN user u ON a.user_id = u.id "
        "WHERE a.title LIKE ? OR a.description LIKE ?",
        (like, like)
    ).fetchall()
