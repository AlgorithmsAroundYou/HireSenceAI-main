# Author: Sai Kumar Kodati

import streamlit as st
from src.generate_sence import GenerateSence
from src.ui_components import render_header, upload_section, display_output
from src.auth import require_auth

# -----------------------
# Route guard (SAFE)
# -----------------------
require_auth()

class HireSence:
    """Page orchestrator for the Agiliad HireSence Streamlit page.

    This class is intentionally thin: UI rendering and PDF parsing live in
    `src.ui_components` and `src.pdf_utils` so they can be unit tested.
    """

    def __init__(self) -> None:
        self.page_title = "Agiliad HireSence"
        self.layout = "wide"
        self.generate_sence = GenerateSence()

    def set_page_config(self) -> None:
        """Set Streamlit page configuration."""
        st.set_page_config(page_title=self.page_title, layout=self.layout)

    def display_header(self) -> None:
        """Render the page header using shared UI components."""
        render_header(
            title=self.page_title,
            subtitle=(
                "Welcome to the Agiliad HireSence platform. "
                "Please upload your files and provide additional information as needed."
            ),
        )

    def display_upload_section(self):
        """Render upload widgets and return collected inputs."""
        return upload_section()

    def display_output(self, submitted, file1, text1, file2, text2, result):
        """Render the output area using shared UI components."""
        display_output(submitted, file1, text1, file2, text2, result)

    def run(self) -> None:
        """Main entrypoint for the page."""
        self.set_page_config()
        self.display_header()

        file1, text1, file2, text2, pdf_text1, pdf_text2 = self.display_upload_section()

        submitted = st.button("Submit")

        if submitted:
            if not (pdf_text1 or text1):
                st.warning("Please upload a resume or provide resume text.")
                return

            if not (pdf_text2 or text2):
                st.warning("Please upload a job description or provide JD text.")
                return

            with st.spinner("Analyzing and generating hiring insights..."):
                result = self.generate_sence.generate_hire_sence(
                    resumeContent=pdf_text1 + text1,
                    job_description=pdf_text2 + text2,
                )

            st.success("✅ Hiring analysis completed!")
            self.display_output(submitted, file1, text1, file2, text2, result)


# -----------------------
# Page entrypoint
# -----------------------
hire_sence = HireSence()
hire_sence.run()
