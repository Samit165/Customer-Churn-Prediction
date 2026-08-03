import streamlit as st

from services.predictor import predict_customer
from services.predictor import get_city_list

def render():

    st.title("🔮 Customer Churn Prediction")

    st.caption("Predict whether a customer is likely to churn.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

        senior = st.selectbox(
            "Senior Citizen",
            ["No", "Yes"]
        )

        partner = st.selectbox(
            "Partner",
            ["No", "Yes"]
        )

        dependents = st.selectbox(
            "Dependents",
            ["No", "Yes"]
        )

        tenure = st.number_input(
            "Tenure (Months)",
            0,
            100,
            12
        )

    with col2:

        contract = st.selectbox(
            "Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )

        internet = st.selectbox(
            "Internet Service",
            [
                "DSL",
                "Fiber optic",
                "No"
            ]
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

        monthly = st.number_input(
            "Monthly Charges",
            0.0,
            500.0,
            70.0
        )

        total = st.number_input(
            "Total Charges",
            0.0,
            10000.0,
            800.0
        )

    st.divider()

    if st.button("🚀 Predict Churn", use_container_width=True):

        customer = {

            "gender": gender,
            "SeniorCitizen": 1 if senior == "Yes" else 0,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "InternetService": internet,
            "Contract": contract,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total,

        }

        prediction, probability = predict_customer(customer)

        st.divider()

        if prediction == 1:

            st.error("⚠️ High Risk Customer")

        else:

            st.success("✅ Customer Likely to Stay")

        st.metric(
            "Churn Probability",
            f"{probability*100:.2f}%"
        )
        city = st.selectbox(
    "City",
    get_city_list(),
    placeholder="Search or select a city..."
)