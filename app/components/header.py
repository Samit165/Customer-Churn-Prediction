import streamlit as st


def show_header():
    st.markdown(
        """
        <div style="text-align:center; padding:20px;">
            <h1 style="color:white;">
                🛡️ ChurnGuard
            </h1>

            <h4 style="color:#94A3B8;">
                Enterprise Customer Retention Intelligence Platform
            </h4>

            <p style="color:#64748B;">
                AI Powered by XGBoost + SHAP
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )