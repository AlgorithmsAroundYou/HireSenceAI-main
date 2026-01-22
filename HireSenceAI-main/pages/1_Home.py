# Author: Sai Kumar Kodati
#

import streamlit as st
from streamlit.logger import get_logger
from Login import login_page

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Agiliad HireSence AI Powered App",
        page_icon="🏚",
        layout="wide"
    )

    st.balloons()
    st.info('This is a purely demo applications', icon="ℹ️")
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


if __name__ == "__main__":
    # -----------------------
    # Router
    # -----------------------
    if not st.session_state.authenticated:
        login_page()
    else:
        run()