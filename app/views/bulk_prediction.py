# pyrefly: ignore [missing-import]
import streamlit as st
import pandas as pd
from utils.csv_validator import validate_csv
from services.bulk_predictor import predict_bulk
from core.database import save_predictions_bulk, log_activity


def render():
    """Render the Bulk Prediction page."""

    st.title("📂 Bulk Prediction")
    st.caption(
        "Upload a CSV file to predict customer churn for multiple customers at once."
    )

    st.divider()

    # ================================================================
    # PHASE 1: If prediction results exist in session state,
    # go straight to results — DO NOT render the file uploader.
    #
    # Why: Streamlit re-runs the entire script on every widget
    # interaction (button click, selectbox change, etc.).
    # When the file uploader is present during these reruns it
    # returns None, hitting the early `return` and wiping the results.
    # By never rendering the file uploader once results exist, this
    # is completely avoided.
    # ================================================================
    if "bulk_prediction_results" in st.session_state:
        _render_results()
        return

    # ================================================================
    # PHASE 2: No results yet — show upload + run form
    # ================================================================
    _render_upload_and_run()


# ------------------------------------------------------------------
# Upload + Run Prediction  (only shown before predictions exist)
# ------------------------------------------------------------------
def _render_upload_and_run():
    """Show the file uploader and run prediction button."""

    uploaded_file = st.file_uploader(
        "Upload Customer CSV",
        type=["csv"],
        help="Upload a CSV file containing customer records.",
        key="bulk_csv_uploader",
    )

    if uploaded_file is None:
        st.info("👆 Upload a CSV file to begin.")
        return

    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Unable to read CSV file.\n\n{e}")
        return

    # File Information
    st.subheader("📄 File Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Filename", uploaded_file.name)
    with c2:
        st.metric("Rows", len(df))
    with c3:
        st.metric("Columns", len(df.columns))

    st.divider()

    # Dataset Preview
    st.subheader("👀 Preview")
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    is_valid, message = validate_csv(df)
    if is_valid:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

    st.divider()

    # Run Prediction Button
    if st.button(
        "🚀 Run Bulk Prediction",
        disabled=not is_valid,
        type="primary",
        use_container_width=True,
        key="btn_run_bulk_predictions",
    ):
        if not is_valid:
            return

        try:
            original_customer_df = df.copy()

            with st.spinner("Running predictions..."):
                result_df = predict_bulk(df)

                result_df.insert(
                    0,
                    "Customer ID",
                    [f"CUST-{i:03d}" for i in range(1, len(result_df) + 1)],
                )

                # Persist everything in session state.
                # After st.rerun() the file uploader is no longer
                # rendered, so it cannot reset and wipe results.
                st.session_state["bulk_customer_data"] = original_customer_df.copy()
                st.session_state["bulk_prediction_results"] = result_df.copy()
                st.session_state["bulk_file_name"] = uploaded_file.name
                st.session_state["bulk_just_ran"] = True

                # Save to Database
                username = st.session_state.get("user", {}).get(
                    "username", "system"
                )

                bulk_records = [
                    (
                        username,
                        row["Customer ID"],
                        row["Prediction"],
                        float(row["Probability"]) / 100,
                        "Bulk",
                    )
                    for _, row in result_df.iterrows()
                ]

                save_predictions_bulk(bulk_records)
                log_activity(username, "Bulk Customer Churn Prediction")

            # Switch page to results-only mode
            st.rerun()

        except Exception as e:
            st.error("Bulk prediction failed.")
            st.exception(e)


# ------------------------------------------------------------------
# Results Section  (shown once predictions are in session state)
# ------------------------------------------------------------------
def _render_results():
    """Render prediction results stored in session state."""

    result_df = st.session_state["bulk_prediction_results"]
    original_customer_df = st.session_state["bulk_customer_data"]
    file_name = st.session_state.get("bulk_file_name", "uploaded file")

    # One-time success message on first run
    if st.session_state.pop("bulk_just_ran", False):
        st.success("✅ Bulk prediction completed successfully!")

    # Header + reset button
    col_info, col_reset = st.columns([4, 1])
    with col_info:
        st.caption(f"📁 **{file_name}** — {len(result_df)} customers")
    with col_reset:
        if st.button(
            "🔄 New Prediction",
            use_container_width=True,
            key="btn_clear_bulk_results",
            help="Clear results and upload a new CSV file.",
        ):
            for k in ["bulk_prediction_results", "bulk_customer_data", "bulk_file_name"]:
                st.session_state.pop(k, None)
            st.rerun()

    st.divider()

    # ---------------------------------
    # Prediction Summary
    # ---------------------------------
    st.subheader("📊 Prediction Summary")

    total_customers = len(result_df)
    churn_count = (result_df["Prediction"] == "Churn").sum()
    stay_count = (result_df["Prediction"] == "No Churn").sum()
    churn_rate = (churn_count / total_customers * 100) if total_customers > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👥 Total Customers", total_customers)
    with c2:
        st.metric("🔴 Predicted Churn", churn_count)
    with c3:
        st.metric("🟢 Predicted Stay", stay_count)
    with c4:
        st.metric("📈 Churn Rate", f"{churn_rate:.2f}%")

    st.divider()

    # ---------------------------------
    # Prediction Results Table
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

    # ---------------------------------
    # Explain Individual Customer
    # ---------------------------------
    st.divider()
    st.subheader("🔍 Explain a Customer")
    st.caption(
        "Select a customer to understand why the model made its prediction using SHAP."
    )

    customer_ids = result_df["Customer ID"].tolist()

    selected_customer_id = st.selectbox(
        "Select Customer ID",
        options=customer_ids,
        key="bulk_explain_customer_select",
    )

    # Retrieve customer data purely from session state DataFrames —
    # no file uploader involved, so changing this dropdown is safe.
    selected_index = result_df.index[
        result_df["Customer ID"] == selected_customer_id
    ][0]

    selected_row = result_df.iloc[selected_index]
    original_customer = original_customer_df.iloc[selected_index].to_dict()

    # Sync session state so Explainability page has the right data
    st.session_state["explain_customer_data"] = original_customer
    st.session_state["explain_source"] = "Bulk Prediction"
    st.session_state["explain_customer_id"] = selected_customer_id

    # Customer overview card
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.metric("Customer", selected_customer_id)
    with sc2:
        st.metric("Prediction", selected_row["Prediction"])
    with sc3:
        st.metric("Churn Probability", f"{selected_row['Probability']}%")

    st.caption(
        "👉 Click the button below to navigate directly to the SHAP explanation."
    )

    if st.button(
        "🔬 View SHAP Explanation Now ➡️",
        type="primary",
        use_container_width=True,
        key="btn_view_shap_explanation",
    ):
        st.session_state.nav_selected = "Explainability"
        st.rerun()

    st.divider()

    # Full Data Expander
    with st.expander("📋 View Full Customer Data"):
        st.caption("Complete customer information used for the bulk prediction.")
        st.dataframe(result_df, use_container_width=True, hide_index=True)

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
