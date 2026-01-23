# Author: Sai Kumar Kodati

import streamlit as st
from src.auth import require_auth
from src.jd import get_all_jd_records, read_jd_content_from_path

# -----------------------
# Route guard (SAFE)
# -----------------------
require_auth()

st.set_page_config(page_title="View JD", layout="wide")

st.markdown("""
# View JD

List of uploaded Job Descriptions stored in the system.
""")

records = get_all_jd_records()

if not records:
    st.info("No JD uploads found.")
else:
    # Display as a table
    import pandas as pd

    df = pd.DataFrame(records)
    st.dataframe(df)

    # Show details for a selected record (display readable JD name)
    options = [(r['id'], r.get('original_name') or f"JD_{r['id']}") for r in records]
    selected = st.selectbox("Select record to view details", options=options, format_func=lambda x: x[1])
    if selected:
        rec = next((r for r in records if r['id'] == selected[0]), None)
    if rec:
        st.markdown("---")
        st.subheader("Record Details")
        # Show friendly metadata only (avoid exposing internal paths/ids)
        st.write(f"Filename: {rec.get('original_name')}")
        st.write(f"Uploaded by: {rec.get('uploaded_by')}")
        st.write(f"Uploaded at: {rec.get('uploaded_at')}")
        if rec.get('status'):
            st.write(f"Status: {rec.get('status')}")
        # If file exists, offer a download link and show extracted content
        import os
        if rec.get('saved_path') and os.path.exists(rec.get('saved_path')):
            with open(rec.get('saved_path'), 'rb') as f:
                st.download_button(label='Download JD file', data=f, file_name=rec.get('original_name') or 'jd.pdf')

            # Extract and display content
            text, err = read_jd_content_from_path(rec.get('saved_path'))
            if err:
                st.error(f"Failed to read JD content: {err}")
            else:
                st.subheader("Extracted JD Content")
                st.text_area("JD Content", value=text, height=400, key=f"jd_content_{rec['id']}")
