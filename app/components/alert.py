import streamlit as st


def success(text):
    st.markdown(
        f'<div class="success-box">{text}</div>',
        unsafe_allow_html=True,
    )


def warning(text):
    st.markdown(
        f'<div class="warning-box">{text}</div>',
        unsafe_allow_html=True,
    )


def danger(text):
    st.markdown(
        f'<div class="danger-box">{text}</div>',
        unsafe_allow_html=True,
    )