# pyrefly: ignore [missing-import]
import streamlit as st


# ── Nav items per role ─────────────────────────────────────────────
MENUS = {
    "Admin": [
        ("Dashboard",       "house-fill"),
        ("Predict",         "graph-up-arrow"),
        ("Bulk Prediction", "cloud-upload-fill"),
        ("Reports",         "bar-chart-fill"),
        ("History",         "clock-history"),
        ("Explainability",  "diagram-3-fill"),
        ("Admin",           "gear-fill"),
        ("About",           "info-circle-fill"),
        ("Logout",          "box-arrow-right"),
    ],
    "Manager": [
        ("Dashboard",       "house-fill"),
        ("Predict",         "graph-up-arrow"),
        ("Bulk Prediction", "cloud-upload-fill"),
        ("Reports",         "bar-chart-fill"),
        ("History",         "clock-history"),
        ("Explainability",  "diagram-3-fill"),
        ("About",           "info-circle-fill"),
        ("Logout",          "box-arrow-right"),
    ],
    "Employee": [
        ("Dashboard",       "house-fill"),
        ("Predict",         "graph-up-arrow"),
        ("History",         "clock-history"),
        ("About",           "info-circle-fill"),
        ("Logout",          "box-arrow-right"),
    ],
}

ICON_MAP = {
    "Dashboard":       "house-fill",
    "Predict":         "graph-up-arrow",
    "Bulk Prediction": "cloud-upload-fill",
    "Reports":         "bar-chart-fill",
    "History":         "clock-history",
    "Explainability":  "diagram-3-fill",
    "Admin":           "gear-fill",
    "About":           "info-circle-fill",
    "Logout":          "box-arrow-right",
}


def show_sidebar(role: str) -> str:
    """Render sidebar and return the selected page name."""

    if "nav_selected" not in st.session_state:
        st.session_state.nav_selected = "Dashboard"

    options = MENUS.get(role, MENUS["Employee"])

    with st.sidebar:

        # Load Bootstrap Icons + global nav styles
        st.markdown(
            """
            <link rel="stylesheet"
                href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

            <style>
            /* ── Branding ───────────────────────────────────── */
            .cg-brand {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 16px 14px 12px;
                margin-bottom: 4px;
            }
            .cg-brand-name {
                font-size: 18px;
                font-weight: 700;
                color: #FFFFFF;
                letter-spacing: 0.4px;
            }

            /* ── Nav button wrapper ─────────────────────────── */
            /* Target the stButton wrapper inside the sidebar */
            section[data-testid="stSidebar"] div.stButton > button {
                display: flex !important;
                align-items: center !important;
                gap: 11px !important;
                width: 100% !important;
                padding: 10px 16px !important;
                margin: 2px 0 !important;
                border-radius: 12px !important;
                border: 1px solid transparent !important;
                background: transparent !important;
                color: #94A3B8 !important;
                font-size: 14px !important;
                font-weight: 500 !important;
                text-align: left !important;
                justify-content: flex-start !important;
                cursor: pointer !important;
                transition:
                    background   0.25s ease,
                    color        0.25s ease,
                    border-color 0.25s ease,
                    box-shadow   0.25s ease,
                    transform    0.25s cubic-bezier(0.4,0,0.2,1) !important;
                box-shadow: none !important;
            }

            /* ── HOVER GLOW ─────────────────────────────────── */
            section[data-testid="stSidebar"] div.stButton > button:hover {
                background    : rgba(37,99,235,0.18) !important;
                color         : #FFFFFF !important;
                border-color  : rgba(96,165,250,0.45) !important;
                transform     : translateX(5px) !important;
                box-shadow    :
                    0 0 10px  rgba(37,99,235,0.55),
                    0 0 24px  rgba(37,99,235,0.28),
                    0 0 48px  rgba(37,99,235,0.12),
                    inset 0 0 14px rgba(37,99,235,0.08) !important;
            }

            /* ── ACTIVE ─────────────────────────────────────── */
            section[data-testid="stSidebar"] div.stButton > button[data-active="true"],
            section[data-testid="stSidebar"] div.stButton > button.cg-active {
                background   : linear-gradient(110deg,#1D4ED8,#2563EB 60%,#3B82F6) !important;
                color        : #FFFFFF !important;
                border-color : rgba(147,197,253,0.40) !important;
                box-shadow   :
                    0 4px 18px rgba(37,99,235,0.50),
                    0 0  28px rgba(37,99,235,0.22) !important;
                transform    : translateX(0) !important;
            }

            /* ── Logout — red glow ──────────────────────────── */
            section[data-testid="stSidebar"] div.stButton > button.cg-logout:hover {
                background   : rgba(239,68,68,0.18) !important;
                border-color : rgba(239,68,68,0.45) !important;
                box-shadow   :
                    0 0 10px rgba(239,68,68,0.55),
                    0 0 24px rgba(239,68,68,0.28) !important;
                color: #FCA5A5 !important;
            }

            /* Remove focus ring */
            section[data-testid="stSidebar"] div.stButton > button:focus {
                box-shadow: none !important;
                outline: none !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # ── Brand header ───────────────────────────────────────────
        st.markdown(
            '<div class="cg-brand">'
            '  <span style="font-size:26px;">🛡️</span>'
            '  <span class="cg-brand-name">ChurnGuard</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        # ── Nav items ──────────────────────────────────────────────
        current = st.session_state.nav_selected

        for label, icon in options:
            is_active = (label == current)
            is_logout = (label == "Logout")

            # Separator before Logout
            if is_logout:
                st.markdown(
                    '<hr style="border:none;border-top:1px solid rgba(148,163,184,0.12);margin:10px 8px 6px;">',
                    unsafe_allow_html=True,
                )

            # Button label: icon + text (Bootstrap icon rendered via HTML is
            # not possible inside st.button, so we use emoji/unicode as fallback)
            EMOJI = {
                "Dashboard":       "🏠",
                "Predict":         "📈",
                "Bulk Prediction": "📤",
                "Reports":         "📊",
                "History":         "🕐",
                "Explainability":  "🔬",
                "Admin":           "⚙️",
                "About":           "ℹ️",
                "Logout":          "🚪",
            }

            btn_label = f"{'  ' if is_active else ''}{EMOJI.get(label,'•')}  {label}"

            clicked = st.button(
                btn_label,
                key=f"nav__{label}",
                use_container_width=True,
            )

            if clicked:
                st.session_state.nav_selected = label
                st.rerun()

        # ── JS to apply active class to the currently selected button ──
        # We inject JS to visually highlight the active button
        active_label = current
        st.markdown(
            f"""
            <script>
            (function() {{
                const btns = window.parent.document.querySelectorAll(
                    'section[data-testid="stSidebar"] div.stButton > button'
                );
                btns.forEach(btn => {{
                    if (btn.innerText.trim().includes({repr(active_label)})) {{
                        btn.style.background = 'linear-gradient(110deg,#1D4ED8,#2563EB 60%,#3B82F6)';
                        btn.style.color = '#FFFFFF';
                        btn.style.borderColor = 'rgba(147,197,253,0.40)';
                        btn.style.boxShadow = '0 4px 18px rgba(37,99,235,0.50),0 0 28px rgba(37,99,235,0.22)';
                    }}
                }});
            }})();
            </script>
            """,
            unsafe_allow_html=True,
        )

    return st.session_state.nav_selected