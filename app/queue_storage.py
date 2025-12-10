# queue_storage.py
"""
Warstwa dostępu do danych dla kolejki rozmów, oparta na SQLite.

Funkcje udostępniane na zewnątrz:
- init_db()                 -> przygotowanie bazy i tabeli
- add_job(description)      -> dodanie zadania ze statusem 'pending'
- take_next_pending_job()   -> pobiera jedno 'pending' i ustawia 'in_progress'
- mark_job_done(job_id)     -> ustawia status zadania na 'done'
"""

import sqlite3
from pathlib import Path
from datetime import datetime

from sqlalchemy.testing.engines import rollback_open_connections

DB_PATH = Path("queue.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=5, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT
            )
            """
        )
    finally:
        conn.close()


# ==== PRODUCER API ====


def add_job(description: str) -> None:
    from uuid import uuid4

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO jobs (id, status, description, created_at)
            VALUES (?, 'pending', ?, ?)
            """,
            (str(uuid4()), description, datetime.now().isoformat(timespec="seconds")),
        )
    finally:
        conn.close()


# ==== CONSUMER API ====


def take_next_pending_job():
    conn = get_connection()
    try:
        conn.execute("BEGIN IMMEDIATE")

        row = conn.execute(
            """
            SELECT rowid AS _rowid, id, description
            FROM jobs
            WHERE status = 'pending'
            ORDER BY created_at LIMIT 1
            """
        ).fetchone()

        if row is None:
            conn.execute("ROLLBACK")
            return None, None

        rowid = row["_rowid"]
        job_id = row["id"]
        description = row["description"]

        conn.execute(
            """
            UPDATE jobs
            SET status     = 'in_progress',
                started_at = ?
            WHERE rowid = ?
            """,
            (datetime.now().isoformat(timespec="seconds"), rowid),
        )

        conn.execute("COMMIT")

        return job_id, description

    except Exception:
        try:
            conn.execute("ROLLBACK")
        except Exception:
            pass
        raise

    finally:
        conn.close()


def mark_job_done(job_id: str) -> None:
    conn = get_connection()
    try:
        conn.execute("""UPDATE jobs
        SET status = 'done',
            finished_at = ?
        WHERE id = ?;""",
                     (datetime.now().isoformat(timespec="seconds"), job_id),)
    finally:
        conn.close()
