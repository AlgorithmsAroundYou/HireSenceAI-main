"""
Repository utilities to read JD upload records from the SQLite database.

This module provides a small, focused API used by Streamlit pages to
fetch JD metadata saved by `src.db`.
"""
from __future__ import annotations

import sqlite3
from typing import List, Dict

from src.db import DB_PATH, init_db


def get_all_jd_records() -> List[Dict]:
    """Return all JD upload records as a list of dictionaries.

    Each dictionary contains: id, saved_path, original_name, uploaded_by, uploaded_at, status
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT id, saved_path, original_name, uploaded_by, uploaded_at, status FROM jd_uploads ORDER BY uploaded_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()
