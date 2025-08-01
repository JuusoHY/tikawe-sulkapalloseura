-- users table
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- announcements table
CREATE TABLE IF NOT EXISTS announcement (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    location TEXT NOT NULL,
    time TEXT NOT NULL,
    slots_needed INTEGER NOT NULL,
    user_id INTEGER NOT NULL REFERENCES user(id)
);

-- registrations (users signing up for an announcement)
CREATE TABLE IF NOT EXISTS registration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    announcement_id INTEGER NOT NULL REFERENCES announcement(id),
    user_id INTEGER NOT NULL REFERENCES user(id)
);

-- classifications (e.g. venue, skill level for an announcement)
CREATE TABLE IF NOT EXISTS classification (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    announcement_id INTEGER NOT NULL REFERENCES announcement(id),
    category TEXT NOT NULL,
    value TEXT NOT NULL
);
