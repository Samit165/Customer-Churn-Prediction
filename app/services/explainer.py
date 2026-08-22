import joblib
import pandas as pd
import shap
import streamlit as st

from core.config import MODEL_PATH, PREPROCESSOR_PATH


@st.cache_resource
def load_explainer():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)

    explainer = shap.TreeExplainer(model)

    return model, preprocessor, explainer


def explain_customer(customer_data: dict):
    """
    Generate a SHAP explanation for one real customer.

    Parameters
    ----------
    customer_data : dict
        Raw customer information entered by the user.

    Returns
    -------
    explanation : shap.Explanation
    probability : float
    prediction : int
    feature_names : list
    """

    model, preprocessor, explainer = load_explainer()

    # Convert the customer's raw data into a DataFrame
    customer_df = pd.DataFrame([customer_data])

    # Apply the SAME preprocessing used by the prediction system
    X = preprocessor.transform(customer_df)

    # Convert sparse matrix to dense if necessary
    if hasattr(X, "toarray"):
        X = X.toarray()

    # Get feature names after preprocessing
    feature_names = [
        name.replace("cat__", "").replace("num__", "")
        for name in preprocessor.get_feature_names_out()
    ]

    X = pd.DataFrame(
        X,
        columns=feature_names
    )

    # Prediction
    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0][1]

    # SHAP explanation
    explanation = explainer(X)

    return (
        explanation[0],
        probability,
        prediction,
        feature_names
    )