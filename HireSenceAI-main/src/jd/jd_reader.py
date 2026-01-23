"""
Utilities to read saved JD file contents from disk.

This module exposes a simple function to return the text content of a
saved JD PDF path. It uses the existing `src.pdf_utils.extract_text_from_pdf`
which expects a file-like object.
"""
from __future__ import annotations

import os
from typing import Tuple, Optional

from src.pdf_utils import extract_text_from_pdf


def read_jd_content_from_path(path: str) -> Tuple[str, Optional[str]]:
    """Read a saved PDF file and return extracted text and optional error.

    Args:
        path: filesystem path to the saved PDF.

    Returns:
        (text, error) same shape as extract_text_from_pdf
    """
    if not path or not os.path.exists(path):
        return "", "File not found"

    try:
        with open(path, "rb") as f:
            text, error = extract_text_from_pdf(f)
            return text, error
    except Exception as e:
        return "", f"Failed to open/read file: {e}"
