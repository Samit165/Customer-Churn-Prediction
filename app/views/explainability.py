import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from utils.feature_mapper import get_display_name
from services.explainer import explain_customer


def render():

    st.title("🧩 Model Explainability")

    st.caption(
        "Understand why ChurnGuard made its prediction using SHAP."
    )

    # =========================================================
    # CUSTOMER DATA FOR EXPLANATION
    # =========================================================

    customer_data = st.session_state.get(
        "explain_customer_data"
    )

    explain_source = st.session_state.get(
        "explain_source",
        "Single Prediction"
    )

    explain_customer_id = st.session_state.get(
        "explain_customer_id"
    )

    # ---------------------------------------------------------
    # Fallback to latest Single Prediction
    # ---------------------------------------------------------

    if customer_data is None:

        customer_data = st.session_state.get(
            "last_customer_data"
        )

        explain_source = "Single Prediction"

    # ---------------------------------------------------------
    # No customer available
    # ---------------------------------------------------------

    if customer_data is None:

        st.info(
            "No customer prediction is available yet."
        )

        st.markdown(
            """
            ### How to use Explainability

            **For Single Prediction**

            1. Go to **Predict**
            2. Enter the customer's information
            3. Click **Predict Churn**
            4. Return to **Explainability**

            **For Bulk Prediction**

            1. Go to **Bulk Prediction**
            2. Upload the customer CSV
            3. Run Bulk Prediction
            4. Select a customer
            5. Click **Explain Selected Customer**
            6. Return to **Explainability**

            ChurnGuard will explain the prediction for that
            exact customer using SHAP.
            """
        )

        return

    # =========================================================
    # EXPLANATION SOURCE
    # =========================================================

    if explain_customer_id:

        st.info(
            f"🔎 Explaining **{explain_customer_id}** "
            f"from **{explain_source}**."
        )

    else:

        st.info(
            f"🔎 Explanation source: **{explain_source}**"
        )

    # =========================================================
    # GENERATE SHAP EXPLANATION
    # =========================================================

    try:

        with st.spinner(
            "Generating customer explanation..."
        ):

            (
                explanation,
                probability,
                prediction,
                feature_names
            ) = explain_customer(customer_data)

    except Exception as e:

        st.error(
            "Unable to generate the SHAP explanation."
        )

        st.exception(e)

        return

    # =========================================================
    # CUSTOMER PREDICTION
    # =========================================================

    st.divider()

    st.subheader(
        "🎯 Customer Prediction"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Prediction",
            "Churn" if prediction == 1 else "No Churn"
        )

    with col2:

        st.metric(
            "Churn Probability",
            f"{probability:.2%}"
        )

    # =========================================================
    # SHAP CONTRIBUTION CHART
    # =========================================================

    st.divider()

    st.subheader(
        "📊 Why did the model make this prediction?"
    )

    st.caption(
        "Positive values push the prediction toward churn. "
        "Negative values push the prediction away from churn."
    )

    # ---------------------------------------------------------
    # Human-readable feature names
    # ---------------------------------------------------------

    display_feature_names = [
        get_display_name(
            feature_name,
            customer_data
        )
        for feature_name in explanation.feature_names
    ]

    # ---------------------------------------------------------
    # Build contribution dataframe
    # ---------------------------------------------------------

    shap_contributions = pd.DataFrame({
        "Feature": display_feature_names,
        "SHAP Value": explanation.values
    })

    # ---------------------------------------------------------
    # Select strongest contributors
    # ---------------------------------------------------------

    shap_contributions["Absolute Impact"] = (
        shap_contributions["SHAP Value"].abs()
    )

    top_contributors = (
        shap_contributions
        .sort_values(
            "Absolute Impact",
            ascending=False
        )
        .head(12)
        .sort_values(
            "SHAP Value",
            ascending=True
        )
    )

    # ---------------------------------------------------------
    # Create chart
    # ---------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    bars = ax.barh(
        top_contributors["Feature"],
        top_contributors["SHAP Value"]
    )

    # Zero reference line

    ax.axvline(
        0,
        linewidth=1
    )

    # ---------------------------------------------------------
    # Add SHAP values
    # ---------------------------------------------------------

    for bar, value in zip(
        bars,
        top_contributors["SHAP Value"]
    ):

        y_position = (
            bar.get_y()
            + bar.get_height() / 2
        )

        if value >= 0:

            ax.text(
                value + 0.01,
                y_position,
                f"+{value:.2f}",
                va="center",
                fontsize=9
            )

        else:

            ax.text(
                value - 0.01,
                y_position,
                f"{value:.2f}",
                va="center",
                ha="right",
                fontsize=9
            )

    # ---------------------------------------------------------
    # Chart labels
    # ---------------------------------------------------------

    ax.set_xlabel(
        "SHAP Impact"
    )

    ax.set_ylabel("")

    ax.set_title(
        "Top Factors Influencing This Prediction"
    )

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.25
    )

    st.pyplot(
        fig,
        clear_figure=True
    )

    plt.close(fig)

    # =========================================================
    # KEY FACTORS
    # =========================================================

    st.divider()

    st.subheader(
        "🎯 Key Factors Behind This Prediction"
    )

    contributions = pd.DataFrame({
        "Feature": explanation.feature_names,
        "SHAP Value": explanation.values,
    })

    # ---------------------------------------------------------
    # Increasing churn factors
    # ---------------------------------------------------------

    positive_factors = (
        contributions[
            contributions["SHAP Value"] > 0
        ]
        .sort_values(
            "SHAP Value",
            ascending=False
        )
        .head(5)
    )

    # ---------------------------------------------------------
    # Reducing churn factors
    # ---------------------------------------------------------

    negative_factors = (
        contributions[
            contributions["SHAP Value"] < 0
        ]
        .sort_values(
            "SHAP Value",
            ascending=True
        )
        .head(5)
    )

    col1, col2 = st.columns(2)

    # =========================================================
    # INCREASING CHURN
    # =========================================================

    with col1:

        st.markdown(
            "### 🔴 Increasing Churn Risk"
        )

        if positive_factors.empty:

            st.info(
                "No significant factors increasing churn."
            )

        else:

            maximum = (
                positive_factors["SHAP Value"]
                .abs()
                .max()
            )

            for _, row in positive_factors.iterrows():

                display_name = get_display_name(
                    row["Feature"],
                    customer_data
                )

                shap_value = row["SHAP Value"]

                st.markdown(
                    f"**{display_name}**"
                )

                st.caption(
                    f"Model impact: +{shap_value:.3f}"
                )

                st.progress(
                    float(
                        abs(shap_value) / maximum
                    )
                )

    # =========================================================
    # REDUCING CHURN
    # =========================================================

    with col2:

        st.markdown(
            "### 🟢 Reducing Churn Risk"
        )

        if negative_factors.empty:

            st.info(
                "No significant factors reducing churn."
            )

        else:

            maximum = (
                negative_factors["SHAP Value"]
                .abs()
                .max()
            )

            for _, row in negative_factors.iterrows():

                display_name = get_display_name(
                    row["Feature"],
                    customer_data
                )

                shap_value = row["SHAP Value"]

                st.markdown(
                    f"**{display_name}**"
                )

                st.caption(
                    f"Model impact: {shap_value:.3f}"
                )

                st.progress(
                    float(
                        abs(shap_value) / maximum
                    )
                )

    # =========================================================
    # FOOTER NOTE
    # =========================================================

    st.caption(
        "Explanation generated using SHAP from the same "
        "customer data used for the prediction."
    )