"""
Utilities to read saved JD file contents from disk.

This module exposes a simple function to return the text content of a
saved JD PDF path. It uses the existing `src.pdf_utils.extract_text_from_pdf`
which expects a file-like object.
"""
from __future__ import annotations

from src.jd.jd_reader import read_jd_content_from_path

__all__ = ["read_jd_content_from_path"]
