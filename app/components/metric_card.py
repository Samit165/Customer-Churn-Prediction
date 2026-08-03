# pyrefly: ignore [missing-import]
import streamlit as st


def metric_card(title, value, icon, color="#2563EB"):
    st.markdown(
        f'<div class="metric-card" style="background:#1E293B; padding:20px; border-radius:16px; border-left:6px solid {color}; box-shadow: 0 4px 20px rgba(0,0,0,0.35); transition: transform 0.2s ease;">'
        f'<div style="font-size:17px; font-weight:600; color:#CBD5E1; display:flex; align-items:center; gap:8px;"><span>{icon}</span><span>{title}</span></div>'
        f'<div style="font-size:32px; font-weight:700; color:#FFFFFF; margin-top:8px;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
