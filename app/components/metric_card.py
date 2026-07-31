import streamlit as st


def metric_card(title, value, color="#2563EB"):

    st.markdown(
        f"""
        <div class="metric-card">

        <h4>{title}</h4>

        <h2 style="color:{color};">
        {value}
        </h2>

        </div>
        """,
        unsafe_allow_html=True,
    )