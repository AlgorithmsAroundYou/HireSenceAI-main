import hashlib
import streamlit as st
from typing import Optional


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


USERS = {
    "admin": hash_password("admin"),
    "user1": hash_password("admin"),
}


def login(username: str, password: str) -> bool:
    """Validate username and password against the USERS store."""
    if username in USERS:
        return USERS[username] == hash_password(password)
    return False


def init_session() -> None:
    """Initialize expected keys in streamlit session_state."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "username" not in st.session_state:
        st.session_state.username = None

    if "just_logged_in" not in st.session_state:
        st.session_state.just_logged_in = False


def require_auth(redirect_to: str = "Login.py") -> None:
    """Guard to ensure the current page requires authentication.

    If the user is not authenticated, redirect to the provided page and stop execution.
    """
    init_session()
    if not st.session_state.authenticated:
        st.switch_page(redirect_to)
        st.stop()


def require_no_auth(redirect_to: str = "pages/1_Home.py") -> None:
    """Guard to ensure the current page is only visible to unauthenticated users.

    If the user is already authenticated, redirect them to the provided page and stop.
    """
    init_session()
    if st.session_state.authenticated:
        st.switch_page(redirect_to)
        st.stop()


def logout() -> None:
    """Log the current user out (clears auth-related session state)."""
    init_session()
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.just_logged_in = False
