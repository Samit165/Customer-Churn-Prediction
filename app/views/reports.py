# pyrefly: ignore [missing-import]

import streamlit as st
import pandas as pd
import plotly.express as px

from core.database import fetch_all


# --------------------------------------------------
# Helpers
# --------------------------------------------------

def _load_predictions():
    """Load all prediction records from the database."""

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
        ORDER BY id ASC
    """)

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame([dict(row) for row in rows])


def _risk_level(probability):
    """Convert churn probability into a risk category."""

    if probability >= 0.70:
        return "High"
    elif probability >= 0.40:
        return "Medium"
    else:
        return "Low"


# --------------------------------------------------
# Main Report
# --------------------------------------------------

def render():

    st.title("📊 Reports")

    st.caption(
        "Customer churn prediction analytics and performance insights."
    )

    # --------------------------------------------------
    # Load Data
    # --------------------------------------------------

    df = _load_predictions()

    if df.empty:

        st.info(
            "📭 No prediction data is available yet. "
            "Generate predictions from the Predict or Bulk Prediction page "
            "to populate this report."
        )

        return

    # --------------------------------------------------
    # Data Preparation
    # --------------------------------------------------

    df["probability"] = pd.to_numeric(
        df["probability"],
        errors="coerce"
    ).fillna(0)

    df["created_at"] = pd.to_datetime(
        df["created_at"],
        errors="coerce"
    )

    df["risk_level"] = df["probability"].apply(
        _risk_level
    )

    # --------------------------------------------------
    # Executive Summary
    # --------------------------------------------------

    st.subheader("📌 Executive Summary")

    total_predictions = len(df)

    churn_count = (
        df["prediction"] == "Churn"
    ).sum()

    stay_count = (
        df["prediction"] == "No Churn"
    ).sum()

    churn_rate = (
        churn_count / total_predictions * 100
        if total_predictions
        else 0
    )

    avg_probability = (
        df["probability"].mean() * 100
        if total_predictions
        else 0
    )

    high_risk = (
        df["risk_level"] == "High"
    ).sum()

    c1, c2, c3, c4, c5 = st.columns(5)

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

    with c5:
        st.metric(
            "⚠️ High Risk",
            high_risk
        )

    st.divider()

    # --------------------------------------------------
    # Prediction Analytics
    # --------------------------------------------------

    st.subheader("📈 Prediction Analytics")

    col1, col2 = st.columns(2)

    # Churn Distribution
    with col1:

        churn_data = (
            df["prediction"]
            .value_counts()
            .reset_index()
        )

        churn_data.columns = [
            "Prediction",
            "Count"
        ]

        fig = px.pie(
            churn_data,
            names="Prediction",
            values="Count",
            hole=0.55,
            title="Churn vs No Churn"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            legend_title=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # Risk Distribution
    with col2:

        risk_data = (
            df["risk_level"]
            .value_counts()
            .reindex(
                ["High", "Medium", "Low"],
                fill_value=0
            )
            .reset_index()
        )

        risk_data.columns = [
            "Risk Level",
            "Count"
        ]

        fig = px.bar(
            risk_data,
            x="Risk Level",
            y="Count",
            title="Risk Level Distribution"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            xaxis_title="",
            yaxis_title="Predictions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------
    # Probability Distribution
    # --------------------------------------------------

    st.subheader("🎯 Churn Probability Distribution")

    probability_data = df.copy()

    probability_data["Probability (%)"] = (
        probability_data["probability"] * 100
    )

    fig = px.histogram(
        probability_data,
        x="Probability (%)",
        nbins=20,
        title="Distribution of Churn Probabilities"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1"),
        xaxis_title="Churn Probability (%)",
        yaxis_title="Number of Predictions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # Prediction Trends
    # --------------------------------------------------

    st.subheader("📅 Prediction Trends")

    trend_df = (
        df.dropna(subset=["created_at"])
        .copy()
    )

    if not trend_df.empty:

        trend_df["Date"] = (
            trend_df["created_at"]
            .dt.date
        )

        daily_predictions = (
            trend_df
            .groupby("Date")
            .size()
            .reset_index(name="Predictions")
        )

        fig = px.line(
            daily_predictions,
            x="Date",
            y="Predictions",
            markers=True,
            title="Daily Prediction Activity"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            xaxis_title="Date",
            yaxis_title="Predictions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "No valid timestamp data is available for trend analysis."
        )

    # --------------------------------------------------
    # Prediction Type Analysis
    # --------------------------------------------------

    st.subheader("📂 Prediction Sources")

    source_data = (
        df["prediction_type"]
        .value_counts()
        .reset_index()
    )

    source_data.columns = [
        "Prediction Type",
        "Count"
    ]

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            source_data,
            x="Prediction Type",
            y="Count",
            title="Single vs Bulk Predictions"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            xaxis_title="",
            yaxis_title="Predictions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        user_data = (
            df["username"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        user_data.columns = [
            "Username",
            "Predictions"
        ]

        fig = px.bar(
            user_data,
            x="Username",
            y="Predictions",
            title="Top Prediction Users"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            xaxis_title="",
            yaxis_title="Predictions"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # --------------------------------------------------
    # Key Insights
    # --------------------------------------------------

    st.subheader("💡 Key Insights")

    if churn_rate >= 30:

        st.warning(
            f"⚠️ The current recorded churn rate is "
            f"**{churn_rate:.2f}%**, indicating a relatively "
            f"high proportion of customers predicted to churn."
        )

    else:

        st.success(
            f"✅ The current recorded churn rate is "
            f"**{churn_rate:.2f}%**."
        )

    st.info(
        f"🎯 The average predicted churn probability is "
        f"**{avg_probability:.2f}%**."
    )

    st.info(
        f"🚨 **{high_risk}** prediction(s) currently fall into "
        f"the High Risk category."
    )

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    st.divider()

    st.subheader("📥 Export Report")

    export_df = df.copy()

    export_df["probability"] = (
        export_df["probability"] * 100
    ).round(2)

    export_df = export_df.rename(
        columns={
            "id": "ID",
            "username": "User",
            "customer_id": "Customer ID",
            "prediction": "Prediction",
            "probability": "Probability (%)",
            "prediction_type": "Prediction Type",
            "created_at": "Created At",
            "risk_level": "Risk Level",
        }
    )

    csv_data = export_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Report CSV",
        data=csv_data,
        file_name="churnguard_report.csv",
        mime="text/csv",
        use_container_width=True
    )