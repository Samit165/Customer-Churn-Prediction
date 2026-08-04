# pyrefly: ignore [missing-import]
import streamlit as st

def render():
    st.title("📂 Bulk Churn Prediction")
    st.caption("Upload CSV files for batch customer churn evaluation.")
    st.file_uploader("Upload Customer Dataset (CSV)", type=["csv"])