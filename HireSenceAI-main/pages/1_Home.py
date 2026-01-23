# Author: Sai Kumar Kodati

import streamlit as st
from streamlit.logger import get_logger
from src.auth import require_auth

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Agiliad HireSence AI Powered App",
        page_icon="🏚",
        layout="wide"
    )

    st.balloons()
    st.info('This is a purely demo application', icon="ℹ️")
    st.write("# Welcome to Agiliad HireSence! 👋")
    st.snow()

    st.markdown(
        """
        Agiliad HireSence is a platform designed to streamline the hiring process using AI.

        ## Features
        - **Job Description Builder**: Create detailed job descriptions effortlessly.
        - **Screening**: AI-driven candidate screening to identify the best fits.
        - **Ranking**: Intelligent ranking of candidates based on job requirements.
        - **Interview Screening Questions**: Generate relevant interview questions.
        """
    )


# -----------------------
# Session state init
# -----------------------
# Guard to ensure only authenticated users can view this page
require_auth()

# If guard passes, run the page
run()
