from db import get_db

def create_announcement(title, description, location, time, slots_needed, user_id, classes):
    """Create announcement and attach selected classes. Returns new announcement id."""
    db = get_db()
    cur = db.execute(
        """INSERT INTO announcement
           (title, description, location, time, slots_needed, user_id)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (title, description, location, time, slots_needed, user_id)
    )
    ann_id = cur.lastrowid
    _set_classes(ann_id, classes)
    db.commit()
    return ann_id

def get_announcements():
    """Return all announcements with their creators’ usernames."""
    return get_db().execute(
        "SELECT a.*, u.username "
        "FROM announcement a JOIN user u ON a.user_id = u.id "
        "ORDER BY a.id DESC"
    ).fetchall()

def get_announcement(announcement_id):
    """Fetch a single announcement by id, including creator username."""
    return get_db().execute(
        "SELECT a.*, u.username "
        "FROM announcement a JOIN user u ON a.user_id = u.id "
        "WHERE a.id = ?",
        (announcement_id,)
    ).fetchone()

def update_announcement(announcement_id, title, description, location, time, slots_needed, classes):
    db = get_db()
    db.execute(
        """UPDATE announcement
           SET title = ?, description = ?, location = ?, time = ?, slots_needed = ?
           WHERE id = ?""",
        (title, description, location, time, slots_needed, announcement_id)
    )
    _set_classes(announcement_id, classes)
    db.commit()

def delete_announcement(announcement_id):
    db = get_db()
    db.execute("DELETE FROM classification WHERE announcement_id = ?", (announcement_id,))
    db.execute("DELETE FROM message WHERE announcement_id = ?", (announcement_id,))
    db.execute("DELETE FROM announcement WHERE id = ?", (announcement_id,))
    db.commit()

def find_announcements(keyword):
    """Search announcements by title or description."""
    like = f"%{keyword}%"
    return get_db().execute(
        "SELECT a.*, u.username "
        "FROM announcement a JOIN user u ON a.user_id = u.id "
        "WHERE a.title LIKE ? OR a.description LIKE ? "
        "ORDER BY a.id DESC",
        (like, like)
    ).fetchall()

# --- Classes (allowed values) and selected classes per announcement ---

def get_all_classes():
    """Return dict: {title: [value, ...]} of all allowed classes."""
    rows = get_db().execute(
        "SELECT title, value FROM classes ORDER BY title, value"
    ).fetchall()
    result = {}
    for r in rows:
        result.setdefault(r["title"], []).append(r["value"])
    return result

def get_classes(announcement_id):
    """Return list of {title, value} for an announcement."""
    return get_db().execute(
        "SELECT category AS title, value FROM classification WHERE announcement_id = ? ORDER BY title, value",
        (announcement_id,)
    ).fetchall()

def _set_classes(announcement_id, classes):
    """Replace classes for an announcement with provided list of (title, value)."""
    db = get_db()
    db.execute("DELETE FROM classification WHERE announcement_id = ?", (announcement_id,))
    for title, value in classes:
        db.execute(
            "INSERT INTO classification (announcement_id, category, value) VALUES (?, ?, ?)",
            (announcement_id, title, value)
        )

# --- Messages (additional info) ---

def add_message(announcement_id, user_id, content):
    db = get_db()
    db.execute(
        "INSERT INTO message (announcement_id, user_id, content) VALUES (?, ?, ?)",
        (announcement_id, user_id, content)
    )
    db.commit()

def get_messages(announcement_id):
    return get_db().execute(
        "SELECT m.id, m.content, m.created_at, u.username "
        "FROM message m JOIN user u ON m.user_id = u.id "
        "WHERE m.announcement_id = ? "
        "ORDER BY m.id DESC",
        (announcement_id,)
    ).fetchall()
