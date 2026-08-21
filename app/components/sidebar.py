# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
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

        # ── Inject hover glow CSS for sidebar nav items ──────────────
        st.markdown(
            """
            <style>
                /* ── Nav link base ───────────────────────────── */
                section[data-testid="stSidebar"] .nav-link {
                    position: relative !important;
                    color: #94A3B8 !important;
                    background: transparent !important;
                    border-radius: 12px !important;
                    margin: 3px 6px !important;
                    padding: 10px 14px !important;
                    border: 1px solid transparent !important;
                    transition:
                        background 0.28s ease,
                        color 0.28s ease,
                        border-color 0.28s ease,
                        box-shadow 0.28s ease,
                        transform 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    overflow: hidden !important;
                    --hover-color: transparent !important;
                }

                /* Kill option_menu's default grey hover completely */
                section[data-testid="stSidebar"] .nav-link:hover,
                section[data-testid="stSidebar"] ul li a.nav-link:hover,
                section[data-testid="stSidebar"] [class*="nav-link"]:hover {
                    background-color: rgba(37, 99, 235, 0.18) !important;
                    background: rgba(37, 99, 235, 0.18) !important;
                    color: #FFFFFF !important;
                    border-color: rgba(96, 165, 250, 0.45) !important;
                    transform: translateX(5px) !important;
                    box-shadow:
                        0 0 12px rgba(37, 99, 235, 0.55),
                        0 0 25px rgba(37, 99, 235, 0.30),
                        0 0 50px rgba(37, 99, 235, 0.14),
                        inset 0 0 18px rgba(37, 99, 235, 0.10) !important;
                }

                /* Hover icon glow */
                section[data-testid="stSidebar"] .nav-link:hover i,
                section[data-testid="stSidebar"] .nav-link:hover svg {
                    color: #60A5FA !important;
                    fill: #60A5FA !important;
                    filter:
                        drop-shadow(0 0 5px rgba(96,165,250,0.90))
                        drop-shadow(0 0 12px rgba(37,99,235,0.70)) !important;
                    transform: scale(1.20) !important;
                    transition: all 0.28s ease !important;
                }

                /* Hover text glow */
                section[data-testid="stSidebar"] .nav-link:hover span {
                    color: #FFFFFF !important;
                    text-shadow: 0 0 10px rgba(147,197,253,0.60) !important;
                    transition: all 0.28s ease !important;
                }

                /* ── ACTIVE / SELECTED ───────────────────────── */
                section[data-testid="stSidebar"] .nav-link-selected,
                section[data-testid="stSidebar"] [class*="nav-link-selected"] {
                    background: linear-gradient(
                        110deg,
                        #1D4ED8 0%,
                        #2563EB 60%,
                        #3B82F6 100%
                    ) !important;
                    color: #FFFFFF !important;
                    border-color: rgba(147, 197, 253, 0.40) !important;
                    box-shadow:
                        0 4px 20px rgba(37, 99, 235, 0.50),
                        0 0 30px rgba(37, 99, 235, 0.25),
                        inset 0 1px 0 rgba(255,255,255,0.12) !important;
                    transform: translateX(0) !important;
                }

                section[data-testid="stSidebar"] .nav-link-selected i,
                section[data-testid="stSidebar"] .nav-link-selected svg {
                    color: #FFFFFF !important;
                    fill: #FFFFFF !important;
                    filter: drop-shadow(0 0 6px rgba(255,255,255,0.55)) !important;
                }

                /* ── ICON base transition ────────────────────── */
                section[data-testid="stSidebar"] .nav-link i,
                section[data-testid="stSidebar"] .nav-link svg {
                    transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1) !important;
                    color: #64748B !important;
                }

                /* ── Logout separator (last item) ────────────── */
                section[data-testid="stSidebar"] ul li:last-child .nav-link {
                    margin-top: 12px !important;
                    border-top: 1px solid rgba(148,163,184,0.12) !important;
                    border-radius: 12px !important;
                }

                section[data-testid="stSidebar"] ul li:last-child .nav-link:hover {
                    background: rgba(239, 68, 68, 0.18) !important;
                    background-color: rgba(239, 68, 68, 0.18) !important;
                    border-color: rgba(239, 68, 68, 0.45) !important;
                    box-shadow:
                        0 0 12px rgba(239,68,68,0.50),
                        0 0 25px rgba(239,68,68,0.25) !important;
                }

                section[data-testid="stSidebar"] ul li:last-child .nav-link:hover i,
                section[data-testid="stSidebar"] ul li:last-child .nav-link:hover svg {
                    color: #F87171 !important;
                    fill: #F87171 !important;
                    filter: drop-shadow(0 0 5px rgba(248,113,113,0.85)) !important;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )

        selected = option_menu(
            "🛡️ ChurnGuard",
            options,
            icons=[icons[item] for item in options],
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                },
                "icon": {
                    "font-size": "16px",
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "border-radius": "12px",
                    "--hover-color": "transparent",
                },
                "nav-link-selected": {
                    "background-color": "#2563EB",
                    "font-weight": "600",
                },
            },
        )

    return selected