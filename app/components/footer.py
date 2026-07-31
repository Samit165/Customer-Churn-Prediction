import streamlit as st


def show_footer():
    st.markdown("---")

    st.markdown(
        """
        <div style="text-align:center;color:gray;font-size:14px;">
            ChurnGuard v1.0
            <br>
            Developed using Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )