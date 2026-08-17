# pyrefly: ignore [missing-import]

import streamlit as st
import pandas as pd

from core.database import (
    fetch_all,
    delete_prediction,
    clear_prediction_history,
    log_activity,
)


def render():

    st.title("📜 Prediction History")

    st.caption(
        "View and manage all customer churn predictions."
    )

    st.divider()

    # ---------------------------------
    # Fetch History
    # ---------------------------------

    rows = fetch_all("""
        SELECT
            id,
            username,
            customer_id,
            prediction,
            probability,
            prediction_type,
            created_at
        FROM predictions
        ORDER BY id DESC
    """)

    if not rows:
        st.info(
            "No prediction history recorded yet. "
            "Use the Predict or Bulk Prediction page "
            "to generate predictions."
        )
        return

    data = [dict(row) for row in rows]

    df = pd.DataFrame(data)

    # ---------------------------------
    # Summary
    # ---------------------------------

    total_predictions = len(df)

    churn_count = (
        df["prediction"] == "Churn"
    ).sum()

    stay_count = (
        df["prediction"] == "No Churn"
    ).sum()

    churn_rate = (
        (churn_count / total_predictions) * 100
        if total_predictions > 0
        else 0
    )

    st.subheader("📊 History Summary")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Total Predictions",
            total_predictions
        )

    with c2:
        st.metric(
            "🔴 Churn",
            churn_count
        )

    with c3:
        st.metric(
            "🟢 No Churn",
            stay_count
        )

    with c4:
        st.metric(
            "📈 Churn Rate",
            f"{churn_rate:.2f}%"
        )

    st.divider()

    # ---------------------------------
    # Filters
    # ---------------------------------

    st.subheader("🔍 Filter History")

    f1, f2, f3 = st.columns(3)

    with f1:

        type_filter = st.selectbox(
            "Prediction Type",
            [
                "All",
                "Single",
                "Bulk"
            ]
        )

    with f2:

        prediction_filter = st.selectbox(
            "Prediction",
            [
                "All",
                "Churn",
                "No Churn"
            ]
        )

    with f3:

        date_filter = st.selectbox(
            "Date",
            [
                "All",
                "Today",
                "Last 7 Days",
                "Last 30 Days"
            ]
        )

    filtered_df = df.copy()

    # Prediction type
    if type_filter != "All":

        filtered_df = filtered_df[
            filtered_df["prediction_type"]
            == type_filter
        ]

    # Prediction
    if prediction_filter != "All":

        filtered_df = filtered_df[
            filtered_df["prediction"]
            == prediction_filter
        ]

    # Date
    if date_filter != "All":

        dates = pd.to_datetime(
            filtered_df["created_at"]
        )

        now = pd.Timestamp.now()

        if date_filter == "Today":

            filtered_df = filtered_df[
                dates.dt.date == now.date()
            ]

        elif date_filter == "Last 7 Days":

            filtered_df = filtered_df[
                dates >= now - pd.Timedelta(days=7)
            ]

        elif date_filter == "Last 30 Days":

            filtered_df = filtered_df[
                dates >= now - pd.Timedelta(days=30)
            ]

    st.divider()

    # ---------------------------------
    # Results
    # ---------------------------------

    st.subheader(
        f"📋 Prediction Records ({len(filtered_df)})"
    )

    if filtered_df.empty:

        st.info(
            "No records match the selected filters."
        )

    else:

        display_df = filtered_df.copy()

        display_df["prediction_type"] = (
            display_df["prediction_type"]
            .map({
                "Single": "👤 Single",
                "Bulk": "📂 Bulk"
            })
            .fillna(display_df["prediction_type"])
        )

        display_df["probability"] = (
            display_df["probability"] * 100
        ).round(2).astype(str) + "%"

        display_df = display_df.rename(
            columns={
                "id": "ID",
                "username": "User",
                "customer_id": "Customer ID",
                "prediction": "Prediction",
                "probability": "Probability",
                "prediction_type": "Type",
                "created_at": "Created At",
            }
        )

        st.dataframe(
            display_df[
                [
                    "ID",
                    "User",
                    "Customer ID",
                    "Prediction",
                    "Probability",
                    "Type",
                    "Created At",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

    # ---------------------------------
    # Admin Management
    # ---------------------------------

    user = st.session_state.get(
        "user",
        {}
    )

    role = user.get(
        "role",
        ""
    )

    if role == "Admin":

        st.divider()

        st.subheader("🛠️ History Management")

        st.caption(
            "Administrative actions permanently remove prediction records."
        )

        # Individual delete
        st.write("### 🗑️ Delete Individual Record")

        prediction_ids = df["id"].tolist()

        selected_id = st.selectbox(
            "Select Prediction ID",
            prediction_ids
        )

        if st.button(
            "🗑️ Delete Selected Record",
            use_container_width=True
        ):

            delete_prediction(
                int(selected_id)
            )

            log_activity(
                user.get("username", "admin"),
                f"Deleted Prediction #{selected_id}"
            )

            st.success(
                f"Prediction #{selected_id} deleted successfully."
            )

            st.rerun()

        # Clear all
        st.write("### 🧹 Clear Entire History")

        confirm_clear = st.checkbox(
            "I understand that this will permanently delete all prediction history."
        )

        if st.button(
            "🧹 Clear All History",
            use_container_width=True,
            disabled=not confirm_clear
        ):

            clear_prediction_history()

            log_activity(
                user.get("username", "admin"),
                "Cleared All Prediction History"
            )

            st.success(
                "All prediction history has been cleared."
            )

            st.rerun()