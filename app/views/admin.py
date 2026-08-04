# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from core.database import fetch_all


def render():
    st.title("⚙️ System Administration")
    st.caption("User and system access management.")
    st.divider()

    rows = fetch_all("SELECT id, username, full_name, email, role, last_login, created_at FROM users")
    if rows:
        st.subheader("Registered Users")
        df = pd.DataFrame([dict(r) for r in rows])
        st.dataframe(df, use_container_width=True, hide_index=True)