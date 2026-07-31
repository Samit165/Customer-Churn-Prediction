import streamlit as st
from streamlit_option_menu import option_menu


def show_sidebar(role):

    menus = {
        "Admin": [
            "Dashboard",
            "Predict",
            "Bulk Prediction",
            "Reports",
            "History",
            "Explainability",
            "Admin",
            "About",
            "Logout",
        ],

        "Manager": [
            "Dashboard",
            "Predict",
            "Bulk Prediction",
            "Reports",
            "History",
            "Explainability",
            "About",
            "Logout",
        ],

        "Employee": [
            "Dashboard",
            "Predict",
            "History",
            "About",
            "Logout",
        ],
    }

    icons = {
        "Dashboard": "house",
        "Predict": "graph-up",
        "Bulk Prediction": "upload",
        "Reports": "bar-chart",
        "History": "clock-history",
        "Explainability": "diagram-3",
        "Admin": "gear",
        "About": "info-circle",
        "Logout": "box-arrow-right",
    }

    options = menus.get(role, menus["Employee"])

    with st.sidebar:

        selected = option_menu(
            "🛡️ ChurnGuard",
            options,
            icons=[icons[item] for item in options],
            default_index=0,
        )

    return selected