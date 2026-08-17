# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from utils.csv_validator import validate_csv
from services.bulk_predictor import predict_bulk
from core.database import save_prediction, log_activity

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
                result_df.insert(
                    0,
                    "Customer ID",
                    [
                        f"CUST-{i:03d}"
                        for i in range(1, len(result_df) + 1)
                    ]
                )
                # ---------------------------------
                # Save Bulk Predictions to Database
                # ---------------------------------

                username = st.session_state.get(
                    "user",
                    {}
                ).get(
                    "username",
                    "system"
                )

                for _, row in result_df.iterrows():

                    prediction_label = row["Prediction"]

                    probability = (
                        float(row["Probability"]) / 100
                    )

                    save_prediction(
                        username,
                        row["Customer ID"],
                        prediction_label,
                        probability,
                        "Bulk"
                        
                    )

                log_activity(
                    username,
                    "Bulk Customer Churn Prediction"
                )
                

            st.success("✅ Bulk prediction completed successfully!")

            st.divider()

            # ---------------------------------
            # Prediction Summary
            # ---------------------------------
            st.subheader("📊 Prediction Summary")

            total_customers = len(result_df)

            churn_count = (
                result_df["Prediction"] == "Churn"
            ).sum()

            stay_count = (
                result_df["Prediction"] == "No Churn"
            ).sum()

            churn_rate = (
                (churn_count / total_customers) * 100
                if total_customers > 0
                else 0
            )

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "👥 Total Customers",
                    total_customers
                )

            with c2:
                st.metric(
                    "🔴 Predicted Churn",
                    churn_count
                )

            with c3:
                st.metric(
                    "🟢 Predicted Stay",
                    stay_count
                )

            with c4:
                st.metric(
                    "📈 Churn Rate",
                    f"{churn_rate:.2f}%"
                )

            st.divider()

            # ---------------------------------
            # Prediction Results
            # ---------------------------------
            st.subheader("🔮 Prediction Results")

            display_columns = [
                "Customer ID",
                "Prediction",
                "Probability",
                "Confidence",
                "Risk Level",
                "Recommendation",
            ]

            st.dataframe(
                result_df[display_columns],
                use_container_width=True,
                hide_index=True,
            )
            st.divider()

            with st.expander("📋 View Full Customer Data"):

                st.caption(
                    "Complete customer information used for the bulk prediction."
                )

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True,
                )

            # ---------------------------------
            # Download Results
            # ---------------------------------
            st.divider()

            st.subheader("📥 Export Results")

            csv_data = result_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Prediction Results",
                data=csv_data,
                file_name="bulk_churn_predictions.csv",
                mime="text/csv",
                use_container_width=True,
            )

        except Exception as e:
            st.error("Bulk prediction failed.")
            st.exception(e)
