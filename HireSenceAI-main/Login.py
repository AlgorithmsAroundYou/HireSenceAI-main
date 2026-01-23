import streamlit as st
from src.auth import login

st.set_page_config(page_title="Agiliad HireSence AI Powered App", layout="centered")

# -----------------------
# Session state init
# -----------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None

if "just_logged_in" not in st.session_state:
    st.session_state.just_logged_in = False


# -----------------------
# Login page
# -----------------------
def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.just_logged_in = True   # 👈 flag
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")


# -----------------------
# Router (SAFE)
# -----------------------
if not st.session_state.authenticated:
    login_page()
else:
    # Navigate only once
    if st.session_state.just_logged_in:
        st.session_state.just_logged_in = False
        st.switch_page("pages/1_Home.py")
