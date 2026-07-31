import streamlit as st

from utils.styling import load_css
from components.sidebar import show_sidebar
from core.auth import authenticate
from components.login import render_login

from core.session import (
    current_user,
    login_user,
    logout_user,
)

from views import (
    dashboard,
    predict,
    bulk_prediction,
    reports,
    history,
    about,
    admin,
    explainability,
)
# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="ChurnGuard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Load CSS
# -----------------------------
load_css()
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# -----------------------------
# Header
# -----------------------------
# show_header()

# st.markdown("---")

# -----------------------------
# Login Form
# -----------------------------
if not st.session_state.authenticated:

    username, password, login_clicked = render_login()

    if login_clicked:

        if not username or not password:
            st.error("Please enter username and password.")

        else:

            user = authenticate(username, password)

            if user:

                login_user(user)

                st.rerun()

            else:

                st.error("Invalid username or password.")

else:

    user = current_user()

    if user is None:
        logout_user()
        st.rerun()

    selected = show_sidebar(user["role"])

    ROUTES = {
        "Dashboard": dashboard.render,
        "Predict": predict.render,
        "Bulk Prediction": bulk_prediction.render,
        "Reports": reports.render,
        "History": history.render,
        "About": about.render,
        "Admin": admin.render,
        "Explainability": explainability.render,
    }

    if selected == "Logout":
        logout_user()
        st.rerun()

    elif selected in ROUTES:
        ROUTES[selected]()
