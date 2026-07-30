"""
==========================================================
ChurnGuard
Login Component
==========================================================

This module renders the login screen.

Responsibilities
----------------
- Display logo
- Display application title
- Display login form
- Return entered credentials

Authentication is handled separately in core/auth.py
"""

from pathlib import Path

import streamlit as st


def render_login():
    """
    Render the ChurnGuard login page.

    Returns
    -------
    tuple
        (username, password, login_clicked)
    """

    # -----------------------------------------------------
    # Logo Path
    # -----------------------------------------------------

    logo_path = (
        Path(__file__).parent.parent
        / "assets"
        / "images"
        / "logo.png"
    )

    # -----------------------------------------------------
    # Center Layout
    # -----------------------------------------------------

    left, center, right = st.columns([1, 1.2, 1])

    with center:

        # -------------------------------------------------
        # Logo
        # -------------------------------------------------
       
        if logo_path.exists():
            st.image(str(logo_path), width=100)
        else:
         st.error("Logo not found")

        # -------------------------------------------------
        # Branding
        # -------------------------------------------------

        st.title("🛡️ ChurnGuard")

        st.caption(
            "Enterprise Customer Retention Intelligence Platform"
        )

        st.caption(
            "AI Powered by XGBoost + SHAP"
        )

        st.markdown("---")

        # -------------------------------------------------
        # Login Form
        # -------------------------------------------------

        username = st.text_input(
            label="Username",
            placeholder="Enter your username",
        )

        password = st.text_input(
            label="Password",
            placeholder="Enter your password",
            type="password",
        )

        login_clicked = st.button(
            "Login",
            use_container_width=True,
        )

        st.markdown("")

        # -------------------------------------------------
        # Footer
        # -------------------------------------------------

        st.caption("Need access? Contact your Administrator")

        st.caption("Version 1.0.0")

    return username, password, login_clicked