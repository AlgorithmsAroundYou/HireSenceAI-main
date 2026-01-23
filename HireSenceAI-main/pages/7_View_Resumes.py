# Author: Sai Kumar Kodati

import streamlit as st
from src.auth import require_auth
from src.resume import get_all_resumes, delete_resume

# -----------------------
# Route guard (SAFE)
# -----------------------
require_auth()

st.set_page_config(page_title="View Resumes", layout="wide")

st.markdown("""
# View Resumes

List of uploaded resumes and the Job Description they are tagged to.
""")

records = get_all_resumes()

if not records:
    st.info("No resumes found.")
else:
    st.subheader("Uploaded Resumes")

    # Display records in a table
    import pandas as pd

    df = pd.DataFrame(records)
    st.dataframe(df)

    # Render action columns directly below the DataFrame so actions are shown inline
    st.markdown("---")
    header_cols = st.columns([3, 2, 2, 2, 1, 1])
    header_cols[0].markdown("**Filename**")
    header_cols[1].markdown("**Tagged JD**")
    header_cols[2].markdown("**Uploaded by**")
    header_cols[3].markdown("**Uploaded at**")
    header_cols[4].markdown("**Download**")
    header_cols[5].markdown("**Delete**")

    import os

    for r in records:
        cols = st.columns([3, 2, 2, 2, 1, 1])
        cols[0].write(r.get('original_name') or f"Resume_{r['id']}")
        cols[1].write(r.get('jd_name'))
        cols[2].write(r.get('uploaded_by'))
        cols[3].write(r.get('uploaded_at'))

        # Download button
        if r.get('saved_path') and os.path.exists(r.get('saved_path')):
            with open(r.get('saved_path'), 'rb') as f:
                cols[4].download_button(label='⬇️', data=f, file_name=r.get('original_name') or 'resume.pdf', key=f"dl_{r['id']}")
        else:
            cols[4].write("N/A")

        # Delete icon button (emoji). Unique key per resume ensures stability.
        if cols[5].button("🗑️", key=f"delete_{r['id']}"):
            try:
                ok = delete_resume(r['id'])
                if ok:
                    st.success(f"Deleted resume {r.get('original_name')}")
                    st.experimental_rerun()
                else:
                    st.error("Failed to delete resume.")
            except Exception as e:
                st.error(f"Error deleting resume: {e}")
