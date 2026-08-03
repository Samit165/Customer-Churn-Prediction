import joblib
import pandas as pd
import streamlit as st


@st.cache_resource
def load_model():
    model = joblib.load("models/churn_model.pkl")
    preprocessor = joblib.load("models/preprocessor.pkl")
    return model, preprocessor


def predict_customer(customer_data: dict):
    """
    Predict customer churn.

    Parameters
    ----------
    customer_data : dict

    Returns
    -------
    prediction : int
    probability : float
    """

    model, preprocessor = load_model()

    df = pd.DataFrame([customer_data])

    X = preprocessor.transform(df)

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0][1]

    return prediction, probability