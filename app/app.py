"""
==========================================================
ChurnGuard
Main Application Entry Point
==========================================================
"""

import streamlit as st

from utils.styling import load_css
from components.login import render_login
from core.auth import authenticate
from core.session import login_user, logout_user

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="ChurnGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# Load Custom CSS
# ---------------------------------------------------------

load_css()

# ---------------------------------------------------------
# Hide Streamlit Default UI
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Hide default multipage navigation */
    section[data-testid="stSidebarNav"]{
        display:none;
    }

    /* Hide sidebar collapse button */
    button[kind="header"]{
        display:none;
    }

    /* Hide Deploy button */
    div[data-testid="stToolbar"]{
        display:none;
    }

    /* Hide Main Menu */
    #MainMenu{
        visibility:hidden;
    }

    footer{
        visibility:hidden;
    }

    header{
        visibility:hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Session State
# ---------------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ---------------------------------------------------------
# Login Screen
# ---------------------------------------------------------

if not st.session_state.authenticated:

    username, password, login = render_login()

    if login:

        user = authenticate(username, password)

        if user:

            login_user(user)

            st.success(
                f"Welcome {user['full_name']}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

else:

    user = st.session_state.user

    st.title("Dashboard")

    st.success(
        f"Welcome {user['full_name']}"
    )

    st.write(f"Username : {user['username']}")
    st.write(f"Role : {user['role']}")
    st.write(f"Email : {user['email']}")

    st.divider()

    if st.button("Logout"):

        logout_user()

        st.rerun()