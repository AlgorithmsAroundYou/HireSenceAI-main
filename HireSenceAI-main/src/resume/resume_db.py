"""
SQLite helpers for storing resume upload metadata.

This mirrors `src.db` but manages a separate `resume_uploads` table and
provides convenience functions used by the resume upload page.
"""
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

from src.db import DB_PATH, init_db


def _ensure_db_dir() -> None:
    Path(os.path.dirname(DB_PATH)).mkdir(parents=True, exist_ok=True)


def init_resume_table() -> None:
    """Create the resume_uploads table if it does not exist."""
    init_db()  # ensure DB file and jd_uploads table exist; safe to call
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS resume_uploads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    saved_path TEXT NOT NULL,
                    original_name TEXT,
                    uploaded_by TEXT,
                    uploaded_at TEXT NOT NULL,
                    job_id INTEGER,
                    status TEXT DEFAULT 'Uploaded'
                )
                """
            )
            # Ensure 'status' column exists for backward compatibility
            cur = conn.execute("PRAGMA table_info(resume_uploads)")
            cols = [r[1] for r in cur.fetchall()]
            if 'status' not in cols:
                try:
                    conn.execute("ALTER TABLE resume_uploads ADD COLUMN status TEXT DEFAULT 'Uploaded'")
                except Exception:
                    pass
    finally:
        conn.close()


def save_resume_record(saved_path: str, original_name: Optional[str], uploaded_by: Optional[str], job_id: Optional[int], status: Optional[str] = "Uploaded") -> int:
    """Insert a resume upload record and return the new record id."""
    init_resume_table()
    conn = sqlite3.connect(DB_PATH)
    try:
        uploaded_at = datetime.utcnow().isoformat() + "Z"
        with conn:
            cur = conn.execute(
                "INSERT INTO resume_uploads (saved_path, original_name, uploaded_by, uploaded_at, job_id, status) VALUES (?, ?, ?, ?, ?, ?)",
                (saved_path, original_name, uploaded_by, uploaded_at, job_id, status),
            )
            return cur.lastrowid
    finally:
        conn.close()


def get_resumes_by_job(job_id: int) -> List[Dict]:
    """Return resume records for a specific job id."""
    init_resume_table()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            "SELECT id, saved_path, original_name, uploaded_by, uploaded_at, job_id FROM resume_uploads WHERE job_id = ? ORDER BY uploaded_at DESC",
            (job_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_all_resumes() -> List[Dict]:
    """Return all resume upload records optionally joined with JD information.

    Each returned dict contains: id, saved_path, original_name, uploaded_by, uploaded_at, job_id, status, jd_name
    """
    init_resume_table()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT r.id, r.saved_path, r.original_name, r.uploaded_by, r.uploaded_at, r.job_id, r.status,
                   j.original_name AS jd_name
            FROM resume_uploads r
            LEFT JOIN jd_uploads j ON r.job_id = j.id
            ORDER BY r.uploaded_at DESC
            """
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_resume(resume_id: int) -> bool:
    """Delete a resume record and its file from disk.

    Returns True if deletion succeeded (DB row removed). File removal is attempted
    but if the file does not exist the DB row is still removed.
    """
    init_resume_table()
    conn = sqlite3.connect(DB_PATH)
    try:
        # fetch saved_path first
        cur = conn.execute("SELECT saved_path FROM resume_uploads WHERE id = ?", (resume_id,))
        row = cur.fetchone()
        saved_path = None
        if row:
            saved_path = row[0]
        # delete DB row
        with conn:
            conn.execute("DELETE FROM resume_uploads WHERE id = ?", (resume_id,))
        # attempt to remove file
        if saved_path:
            try:
                if os.path.exists(saved_path):
                    os.remove(saved_path)
            except Exception:
                # ignore file removal errors; DB row already removed
                pass
        return True
    finally:
        conn.close()
