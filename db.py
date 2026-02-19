import hashlib
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from config import DB_PATH

# Each entry is a migration that brings the DB from version (index) to (index+1).
# Never edit existing entries — only append new ones.
MIGRATIONS = [
    # v0 → v1: initial schema
    """
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
    """,
    # v1 → v2: add PIN protection
    "ALTER TABLE users ADD COLUMN pin_hash TEXT;",
    # v2 → v3: add duress mode
    "ALTER TABLE users ADD COLUMN duress_mode INTEGER DEFAULT 0;",
]


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
        version = conn.execute("PRAGMA user_version").fetchone()[0]
        for i, migration in enumerate(MIGRATIONS[version:], start=version):
            conn.executescript(migration)
            conn.execute(f"PRAGMA user_version = {i + 1}")


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
            (datetime.now(timezone.utc), user_id),
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


def suppress_stale_alert(user_id: int):
    """If user is already past their deadline and unalerted, mark alerted so newly
    added watchers don't receive an alert for a check-in that predates them."""
    with get_db() as conn:
        conn.execute(
            """
            UPDATE users SET alerted = 1
            WHERE user_id = ?
              AND last_checkin IS NOT NULL
              AND alerted = 0
              AND datetime(last_checkin, '+' || deadline_hours || ' hours') < datetime('now')
            """,
            (user_id,),
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


def has_watchers(user_id: int) -> bool:
    """Check if a user has at least one watcher."""
    with get_db() as conn:
        row = conn.execute(
            "SELECT 1 FROM recipients WHERE user_id = ? LIMIT 1", (user_id,)
        ).fetchone()
        return row is not None


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


def _hash_pin(user_id: int, pin: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), str(user_id).encode(), 100_000
    ).hex()


def set_pin(user_id: int, pin: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET pin_hash = ? WHERE user_id = ?",
            (_hash_pin(user_id, pin), user_id),
        )


def get_pin_hash(user_id: int) -> str | None:
    with get_db() as conn:
        row = conn.execute(
            "SELECT pin_hash FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return row["pin_hash"] if row else None


def verify_pin(user_id: int, pin: str) -> bool:
    stored = get_pin_hash(user_id)
    if not stored:
        return False
    return stored == _hash_pin(user_id, pin)


def clear_pin(user_id: int):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET pin_hash = NULL, duress_mode = 0 WHERE user_id = ?",
            (user_id,),
        )


def get_duress_mode(user_id: int) -> bool:
    with get_db() as conn:
        row = conn.execute(
            "SELECT duress_mode FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
        return bool(row["duress_mode"]) if row else False


def set_duress_mode(user_id: int, enabled: bool):
    with get_db() as conn:
        conn.execute(
            "UPDATE users SET duress_mode = ? WHERE user_id = ?",
            (1 if enabled else 0, user_id),
        )
