"""
Local file storage helpers (moved into src.common).

This is the same implementation as the former top-level `src/file_store.py`.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional


def ensure_dir(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def _timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def save_uploaded_file(uploaded_file, dest_dir: str = "data/uploads") -> str:
    """Save a Streamlit uploaded file to disk.

    Args:
        uploaded_file: the uploaded file object from Streamlit (has .read() and .name)
        dest_dir: destination directory (relative to repo root)

    Returns:
        Absolute path to the saved file.
    """
    ensure_dir(dest_dir)

    name = getattr(uploaded_file, "name", None) or f"uploaded_{_timestamp()}"
    dest_path = os.path.abspath(os.path.join(dest_dir, name))

    # uploaded_file may provide getbuffer() or read(); handle both.
    try:
        data = uploaded_file.getbuffer()
    except Exception:
        # fallback to read()
        uploaded_file.seek(0)
        data = uploaded_file.read()

    with open(dest_path, "wb") as f:
        if isinstance(data, memoryview):
            f.write(data.tobytes())
        else:
            f.write(data)

    return dest_path


def save_text_file(text: str, filename: Optional[str] = None, dest_dir: str = "data/uploads") -> str:
    """Save a text string to a .txt file on disk.

    If filename is omitted, a timestamped name is generated.
    Returns the absolute path to the saved file.
    """
    ensure_dir(dest_dir)

    if not filename:
        filename = f"jd_{_timestamp()}.txt"

    dest_path = os.path.abspath(os.path.join(dest_dir, filename))

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(text or "")

    return dest_path
