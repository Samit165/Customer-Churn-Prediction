# pyrefly: ignore [missing-import]
import streamlit as st

from services.predictor import (
    get_city_list,
    predict_customer
)
from core.database import save_prediction, log_activity


def render():

    st.title("🔮 Customer Churn Prediction")

    st.caption("Predict whether a customer is likely to churn based on profile, services, and billing.")

    top_clicked = st.button("🚀 Predict Churn Now", type="primary", use_container_width=True, key="top_predict_btn")

    st.divider()

    st.subheader("👤 Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        city = st.selectbox(
            "City",
            get_city_list()
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        senior = st.selectbox(
            "Senior Citizen",
            ["No", "Yes"]
        )

    with col2:

        partner = st.selectbox(
            "Partner",
            ["No", "Yes"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["No", "Yes"]
        )

        tenure = st.number_input(
            "Tenure Months",
            min_value=0,
            max_value=100,
            value=12
        )
    st.divider()
    st.subheader("📡 Services")

    col1, col2 = st.columns(2)

    with col1:
        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["Yes", "No", "No phone service"]
        )

        internet_service = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

    with col2:
        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )
    st.subheader("💳 Account Information")

    col1, col2 = st.columns(2)

    with col1:
        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        paperless = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

    with col2:
        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=800.0
        )
    
    

    st.divider()
    bottom_clicked = st.button("🚀 Predict Churn", type="primary", use_container_width=True, key="bottom_predict_btn")

    if top_clicked or bottom_clicked:

        customer_data = {
            "City": city,
            "Gender": gender,
            "Senior Citizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "Tenure Months": tenure,
            "Phone Service": phone_service,
            "Multiple Lines": multiple_lines,
            "Internet Service": internet_service,
            "Online Security": online_security,
            "Online Backup": online_backup,
            "Device Protection": device_protection,
            "Tech Support": tech_support,
            "Streaming TV": streaming_tv,
            "Streaming Movies": streaming_movies,
            "Contract": contract,
            "Paperless Billing": paperless,
            "Payment Method": payment_method,
            "Monthly Charges": monthly_charges,
            "Total Charges": total_charges,
        }

        prediction, probability, confidence = predict_customer(customer_data)
        
        st.session_state["last_customer_data"] = customer_data
        st.session_state["last_prediction"] = prediction
        st.session_state["last_probability"] = probability

        st.divider()

        if prediction == 1:

            st.error("⚠️ High Risk of Churn")
            risk = "HIGH"
            recommendation = (
                "Contact the customer immediately and "
                "offer a retention incentive."
            )

        else:

            st.success("✅ Customer Likely to Stay")

            risk = "LOW"

            recommendation = (
                "Customer is likely to remain. "
                "Continue normal engagement."
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Probability",
                f"{probability * 100:.2f}%"
            )

        with c2:
            st.metric(
                "Confidence",
                f"{confidence * 100:.2f}%"
            )

        with c3:
            st.metric(
                "Risk Level",
                risk
            )

        st.info(f"💡 Recommendation: {recommendation}")

        username = st.session_state.get("user", {}).get("username", "system")
        pred_label = "Churn" if prediction == 1 else "No Churn"
        save_prediction(username, "CUST-SINGLE", pred_label, float(probability))
        log_activity(username, "Single Customer Churn Prediction")
