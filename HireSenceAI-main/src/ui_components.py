"""
Reusable Streamlit UI components for HireSence pages.

This module centralizes header rendering, upload widgets and output display so
pages become thin orchestrators.
"""

from typing import Any, Optional, Tuple
import streamlit as st
from src.pdf_utils import extract_text_from_pdf


def render_header(title: str, subtitle: str) -> None:
    """Render the page header.

    Args:
        title: Main page title.
        subtitle: Subtitle / description text.
    """
    st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>{subtitle}</p>", unsafe_allow_html=True)
    st.markdown("---")


def upload_section() -> Tuple[Optional[Any], str, Optional[Any], str, str, str]:
    """Render two-column upload section for resumes and job descriptions.

    Returns:
        Tuple containing (file1, text1, file2, text2, extracted_pdf_text1, extracted_pdf_text2)
    """
    col1, col2 = st.columns(2)

    # Resumes column
    with col1:
        st.subheader("Resumes")
        file1 = st.file_uploader(
            "Choose a PDF file for Resumes",
            key="file1",
            type=["pdf"]
        )

        pdf_text1 = ""
        if file1 is not None:
            pdf_text1, error = extract_text_from_pdf(file1)
            if error:
                st.error("Failed to read resume PDF.")
            else:
                st.text_area(
                    "Extracted Resume Content",
                    pdf_text1,
                    key="pdf_text1",
                    height=200
                )

        text1 = st.text_area(
            "Optional Information for Resume Content",
            key="text1",
            height=200
        )

    # Job Descriptions column
    with col2:
        st.subheader("Job Descriptions")
        file2 = st.file_uploader(
            "Choose a PDF file for Job Descriptions",
            key="file2",
            type=["pdf"]
        )

        pdf_text2 = ""
        if file2 is not None:
            pdf_text2, error = extract_text_from_pdf(file2)
            if error:
                st.error("Failed to read JD PDF.")
            else:
                st.text_area(
                    "Extracted Job Description Content",
                    pdf_text2,
                    key="pdf_text2",
                    height=200
                )

        text2 = st.text_area(
            "Optional Information for Job Description Content",
            key="text2",
            height=200
        )

    return file1, text1, file2, text2, pdf_text1, pdf_text2


def display_output(submitted: bool, file1: Optional[Any], text1: str, file2: Optional[Any], text2: str, result: str) -> None:
    """Render the output section.

    Args:
        submitted: Whether the user pressed the submit button.
        file1: Uploaded resume file or None.
        text1: Optional resume text.
        file2: Uploaded JD file or None.
        text2: Optional JD text.
        result: The result string to display.
    """
    st.markdown("---")
    st.subheader("Output")

    if submitted:
        st.write("Generating hiring scene...")
        st.write(result)
        st.markdown("---")
        st.write("Files and information submitted successfully!")

        if file1:
            st.write(f"Resume file: {getattr(file1, 'name', str(file1))}")
        if file2:
            st.write(f"JD file: {getattr(file2, 'name', str(file2))}")
