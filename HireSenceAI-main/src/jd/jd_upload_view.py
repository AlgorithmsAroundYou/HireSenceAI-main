from __future__ import annotations

import streamlit as st
from typing import Tuple, Optional

from src.common.file_store import save_uploaded_file
from src.db import save_jd_record


def jd_upload_component(key: Optional[str] = None) -> Optional[object]:
    """Render a small upload component and return the uploaded file object or None.

    This mirrors the previous small UI used in pages but kept as a reusable
    function for tests and other pages.
    """
    file = st.file_uploader("Choose a PDF file for Job Description", key=(key or "jd_file_only"), type=["pdf"])
    return file


def render_jd_upload() -> None:
    st.markdown("""
    # Upload JD

    Use this page to upload a single Job Description PDF. No extraction or text entry is required here — only upload and save.
    """)

    file = jd_upload_component()
    if file:
        st.write(f"Selected file: {getattr(file, 'name', str(file))}")

    submitted = st.button("Upload JD")

    if submitted:
        if not file:
            st.warning("Please choose a JD PDF file before uploading.")
        else:
            try:
                saved_path = save_uploaded_file(file)

                # record metadata in DB
                try:
                    uploader = None
                    try:
                        uploader = st.session_state.get("username")
                    except Exception:
                        uploader = None

                    record_id = save_jd_record(
                        saved_path=saved_path,
                        original_name=getattr(file, "name", None),
                        uploaded_by=uploader,
                    )
                    st.success("JD uploaded and saved successfully!")
                    st.write(f"Saved to: {saved_path}")
                    st.write(f"DB record id: {record_id}")
                except Exception as db_e:
                    st.error(f"File saved but failed to record metadata: {db_e}")

            except Exception as e:
                st.error(f"Failed to save uploaded file: {e}")
