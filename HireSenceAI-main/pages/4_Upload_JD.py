# Author: Sai Kumar Kodati

import streamlit as st
from src.auth import require_auth
from src.file_store import save_uploaded_file
from src.db import save_jd_record

# -----------------------
# Route guard (SAFE)
# -----------------------
require_auth()

st.set_page_config(page_title="Upload JD", layout="wide")

st.markdown("""
# Upload JD

Use this page to upload a single Job Description PDF. No extraction or text entry is required here — only upload and save.
""")

file = st.file_uploader("Choose a PDF file for Job Description", key="jd_file_only", type=["pdf"])

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
