"""
==========================================================
ChurnGuard
Session Management
==========================================================
"""

import streamlit as st


def login_user(user):
    """
    Store authenticated user in the session.
    """

    st.session_state.authenticated = True

    st.session_state.user = {
        "id": user["id"],
        "username": user["username"],
        "full_name": user["full_name"] if user["full_name"] else user["username"],
        "email": user["email"] if user["email"] else "",
        "role": user["role"],
        "status": user["status"],
    }


def logout_user():
    """
    Clear current session.
    """

    st.session_state.authenticated = False

    if "user" in st.session_state:
        del st.session_state.user


def current_user():
    """
    Return current logged-in user.
    """

    return st.session_state.get("user")