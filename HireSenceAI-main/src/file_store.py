"""
Local file storage helpers.

This module provides small utilities to persist Streamlit uploaded files
and plain text to a local directory under the project. It is intentionally
simple and synchronous — suitable for small demo apps.
"""
from __future__ import annotations

from src.common.file_store import save_uploaded_file, save_text_file

__all__ = ["save_uploaded_file", "save_text_file"]
