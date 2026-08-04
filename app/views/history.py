# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from core.database import fetch_all


def render():
    st.title("📜 Prediction History")
    st.caption("Log of all customer churn predictions.")
    st.divider()

    rows = fetch_all("SELECT id, username, customer_id, prediction, probability, created_at FROM predictions ORDER BY id DESC")

    if rows:
        data = [dict(r) for r in rows]
        df = pd.DataFrame(data)
        df["probability"] = df["probability"].apply(lambda p: f"{p * 100:.2f}%" if pd.notnull(p) else "N/A")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No prediction history recorded yet. Use the Predict page to generate predictions.")