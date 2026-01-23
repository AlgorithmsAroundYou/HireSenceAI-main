# Author: Sai Kumar Kodati

import streamlit as st
from src.auth import require_auth
from src.jd import get_all_jd_records
from src.common.file_store import save_uploaded_file
from src.resume import save_resume_record

# -----------------------
# Route guard (SAFE)
# -----------------------
require_auth()

st.set_page_config(page_title="Upload Resumes", layout="wide")

st.markdown("""
# Upload Resumes

Select a Job Description, then upload up to 10 resume PDFs to associate with that JD.
""")

# fetch JDs for dropdown
records = get_all_jd_records()
options = [(r['id'], r.get('original_name') or f"JD_{r['id']}") for r in records]
selected_job_id = None
if options:
    selected = st.selectbox("Select Job Description to tag resumes", options=options, format_func=lambda x: x[1])
    selected_job_id = selected[0]
else:
    st.warning("No Job Descriptions found. Please upload a JD first.")

uploaded_files = st.file_uploader("Choose up to 10 PDF resumes", accept_multiple_files=True, type=["pdf"], key="resume_uploads")

if uploaded_files:
    st.write(f"Selected {len(uploaded_files)} files")

submitted = st.button("Upload Resumes")

if submitted:
    if not selected_job_id:
        st.warning("Please select a Job Description first.")
    elif not uploaded_files:
        st.warning("Please select at least one resume to upload.")
    elif len(uploaded_files) > 10:
        st.warning("Please upload a maximum of 10 resumes at once.")
    else:
        saved_names = []
        for f in uploaded_files:
            try:
                path = save_uploaded_file(f, dest_dir="data/resumes")
                uploader = st.session_state.get("username") if "username" in st.session_state else None
                rec_id = save_resume_record(path, getattr(f, 'name', None), uploader, selected_job_id)
                # record only the original filename for display; do not show paths or ids
                saved_names.append(getattr(f, 'name', None) or 'unnamed')
            except Exception as e:
                st.error(f"Failed to save {getattr(f, 'name', str(f))}: {e}")

        if saved_names:
            st.success(f"Saved {len(saved_names)} resume(s)")
            st.write("Uploaded files:")
            for name in saved_names:
                st.write(f"- {name}")
