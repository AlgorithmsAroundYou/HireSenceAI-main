"""
Simple SQLite helper for storing uploaded JD metadata.

This module creates a lightweight database at data/db.sqlite3 and
exposes a function to save JD upload records.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = os.path.abspath(os.path.join("data", "db.sqlite3"))


def _ensure_db_dir() -> None:
    Path(os.path.dirname(DB_PATH)).mkdir(parents=True, exist_ok=True)


def _get_conn() -> sqlite3.Connection:
    _ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create the JD uploads table if it does not exist and ensure 'status' column exists."""
    conn = _get_conn()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jd_uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    saved_path TEXT NOT NULL,
                    original_name TEXT,
                    uploaded_by TEXT,
                    uploaded_at TEXT NOT NULL,
                    status TEXT DEFAULT 'Uploaded'
                )
                """
            )
            # Ensure 'status' column exists (for migrations from older schema)
            cur = conn.execute("PRAGMA table_info(jd_uploads)")
            cols = [r[1] for r in cur.fetchall()]
            if 'status' not in cols:
                try:
                    conn.execute("ALTER TABLE jd_uploads ADD COLUMN status TEXT DEFAULT 'Uploaded'")
                except Exception:
                    # If ALTER fails, ignore and continue — table may already be in desired state
                    pass
    finally:
        conn.close()


def save_jd_record(saved_path: str, original_name: Optional[str], uploaded_by: Optional[str], status: Optional[str] = "Uploaded") -> int:
    """Insert a JD upload record and return the new record id.

    Args:
        saved_path: absolute path where the file was saved
        original_name: the original filename provided by the uploader
        uploaded_by: username or identifier of the uploader
        status: status label for the upload (default: 'Uploaded')

    Returns:
        Integer id of the inserted row.
    """
    init_db()
    conn = _get_conn()
    try:
        uploaded_at = datetime.utcnow().isoformat() + "Z"
        with conn:
            cur = conn.execute(
                "INSERT INTO jd_uploads (saved_path, original_name, uploaded_by, uploaded_at, status) VALUES (?, ?, ?, ?, ?)",
                (saved_path, original_name, uploaded_by, uploaded_at, status),
            )
            return cur.lastrowid
    finally:
        conn.close()
