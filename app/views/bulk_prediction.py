# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from utils.csv_validator import validate_csv
from services.bulk_predictor import predict_bulk


def render():
    """Render the Bulk Prediction page."""

    st.title("📂 Bulk Prediction")
    st.caption(
        "Upload a CSV file to predict customer churn for multiple customers at once."
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"],
        help="Upload a CSV file containing customer records.",
    )

    if uploaded_file is None:
        st.info("👆 Upload a CSV file to begin.")
        return

    try:
        df = pd.read_csv(uploaded_file)

    except Exception as e:
        st.error(f"Unable to read CSV file.\n\n{e}")
        return

    # -----------------------------
    # File Information
    # -----------------------------
    st.subheader("📄 File Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Filename", uploaded_file.name)

    with c2:
        st.metric("Rows", len(df))

    with c3:
        st.metric("Columns", len(df.columns))

    st.divider()

    # -----------------------------
    # Dataset Preview
    # -----------------------------
    st.subheader("👀 Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True,
    )

    is_valid, message = validate_csv(df)

    if is_valid:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

    st.divider()

    # -----------------------------
    # Run Prediction
    # -----------------------------
    with st.form("bulk_prediction_form"):
        submitted = st.form_submit_button(
            "🚀 Run Bulk Prediction",
            disabled=not is_valid,
            use_container_width=True,
        )

    if submitted and is_valid:
        try:
            with st.spinner("Running predictions..."):
                result_df = predict_bulk(df)

            st.success("✅ Bulk prediction completed successfully!")

            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True,
            )

        except Exception as e:
            st.error("Bulk prediction failed.")
            st.exception(e)