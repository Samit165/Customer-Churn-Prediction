import streamlit as st

from components.metric_card import metric_card
from components.charts import (
    churn_pie,
    prediction_trend,
    model_performance
)


def render():

    st.title("📊 Dashboard")

    st.caption("Customer Churn Analytics Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Total Users",
            "254",
            "👤",
            "#3B82F6"
        )

    with c2:
        metric_card(
            "Predictions",
            "1,348",
            "🔮",
            "#10B981"
        )

    with c3:
        metric_card(
            "Churn Rate",
            "26.5%",
            "⚠️",
            "#F59E0B"
        )

    with c4:
        metric_card(
            "Accuracy",
            "85.7%",
            "🎯",
            "#8B5CF6"
        )

    st.divider()

    col1, col2 = st.columns([2,1])

    with col1:
        st.subheader("Prediction Trend")
        st.plotly_chart(
            prediction_trend(),
            use_container_width=True
        )

    with col2:
        st.subheader("Churn Distribution")
        st.plotly_chart(
            churn_pie(),
            use_container_width=True
        )

    st.divider()

    st.subheader("Model Performance")

    st.plotly_chart(
        model_performance(),
        use_container_width=True
    )

    st.divider()

    st.subheader("Recent Activity")

    st.dataframe(
        [
            {
                "Time":"10:15",
                "Activity":"Prediction Completed"
            },
            {
                "Time":"09:52",
                "Activity":"Admin Login"
            },
            {
                "Time":"09:30",
                "Activity":"Bulk Prediction"
            },
            {
                "Time":"09:05",
                "Activity":"Report Generated"
            },
        ],
        use_container_width=True,
        hide_index=True
    )