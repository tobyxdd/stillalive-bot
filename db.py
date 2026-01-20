import sqlite3
from contextlib import contextmanager
from datetime import datetime

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    message TEXT,
    interval_hours INTEGER DEFAULT 24,
    deadline_hours INTEGER DEFAULT 48,
    reminder_hour INTEGER DEFAULT 9,
    reminder_before INTEGER DEFAULT 6,
    last_checkin TIMESTAMP,
    alerted INTEGER DEFAULT 0,
    language TEXT DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    watcher_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, watcher_id)
);

CREATE TABLE IF NOT EXISTS invites (
    code TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
"""


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.executescript(SCHEMA)


def get_user(user_id: int) -> dict | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None


def upsert_user(user_id: int, username: str = None, **fields):
    with get_db() as conn:
        existing = conn.execute(
            "SELECT 1 FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        if existing:
            if fields:
                sets = ", ".join(f"{k} = ?" for k in fields)
                conn.execute(
                    f"UPDATE users SET {sets} WHERE user_id = ?",
                    (*fields.values(), user_id),
                )
        else:
            conn.execute(
                "INSERT INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username),
            )


def checkin(user_id: int):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET last_checkin = ?, alerted = 0 WHERE user_id = ?",
            (datetime.utcnow(), user_id),
        )


def get_users_past_deadline() -> list[dict]:
    """Get users who are past deadline and not yet alerted."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT * FROM users 
            WHERE last_checkin IS NOT NULL 
              AND alerted = 0
              AND datetime(last_checkin, '+' || deadline_hours || ' hours') < datetime('now')
        """).fetchall()
        return [dict(r) for r in rows]


def mark_alerted(user_id: int):
    with get_db() as conn:
        conn.execute("UPDATE users SET alerted = 1 WHERE user_id = ?", (user_id,))


def get_users_needing_deadline_reminder() -> list[dict]:
    """Get users approaching deadline (within reminder_before hours)."""
    with get_db() as conn:
        rows = conn.execute("""
            SELECT * FROM users 
            WHERE last_checkin IS NOT NULL 
              AND alerted = 0
              AND datetime(last_checkin, '+' || (deadline_hours - reminder_before) || ' hours') < datetime('now')
              AND datetime(last_checkin, '+' || deadline_hours || ' hours') > datetime('now')
        """).fetchall()
        return [dict(r) for r in rows]


# Invite functions
def create_invite(user_id: int, code: str):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM invites WHERE user_id = ?", (user_id,)
        )  # One active invite per user
        conn.execute(
            "INSERT INTO invites (code, user_id) VALUES (?, ?)", (code, user_id)
        )


def get_invite(code: str) -> dict | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM invites WHERE code = ?", (code,)).fetchone()
        return dict(row) if row else None


def delete_invite(code: str):
    with get_db() as conn:
        conn.execute("DELETE FROM invites WHERE code = ?", (code,))


# Recipient/watcher functions
def add_watcher(user_id: int, watcher_id: int):
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO recipients (user_id, watcher_id) VALUES (?, ?)",
            (user_id, watcher_id),
        )


def remove_watcher(user_id: int, watcher_id: int):
    with get_db() as conn:
        conn.execute(
            "DELETE FROM recipients WHERE user_id = ? AND watcher_id = ?",
            (user_id, watcher_id),
        )


def get_watchers(user_id: int) -> list[int]:
    """Get list of watcher user_ids for a user."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT watcher_id FROM recipients WHERE user_id = ?", (user_id,)
        ).fetchall()
        return [r["watcher_id"] for r in rows]


def get_watching(watcher_id: int) -> list[dict]:
    """Get list of users that watcher_id is watching (with their info)."""
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT u.* FROM users u
            JOIN recipients r ON u.user_id = r.user_id
            WHERE r.watcher_id = ?
        """,
            (watcher_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_all_users() -> list[dict]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM users").fetchall()
        return [dict(r) for r in rows]
