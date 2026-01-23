"""
Streamlit view for uploading a single Job Description (JD).

This module provides a small, focused UI view to upload a JD PDF
and/or paste optional JD text. It returns the uploaded file object,
any user-provided text, and the extracted PDF text (if a PDF was
uploaded).

Taken from `src/jd_upload_ui_component.py`.
"""
from src.jd.jd_upload_view import render_jd_upload, jd_upload_component

__all__ = ["render_jd_upload", "jd_upload_component"]
