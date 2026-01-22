import streamlit as st
from src.auth import login

st.set_page_config(page_title="Secure App", layout="centered")

# -----------------------
# Session state init
# -----------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = None


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
            st.success("Login successful!")
            st.switch_page("pages/1_Home.py")
        else:
            st.error("Invalid username or password")


# -----------------------
# Router
# -----------------------
if not st.session_state.authenticated:
    login_page()
else:
    st.switch_page("pages/1_Home.py")
