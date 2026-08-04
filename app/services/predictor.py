import joblib
import pandas as pd
# pyrefly: ignore [missing-import]
import streamlit as st

from core.config import MODEL_PATH, PREPROCESSOR_PATH


@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return model, preprocessor


@st.cache_data
def get_city_list():
    _, preprocessor = load_model()

    encoder = preprocessor.named_transformers_["cat"]

    categorical_columns = preprocessor.transformers_[1][2]

    city_index = list(categorical_columns).index("City")

    return sorted(encoder.categories_[city_index].tolist())


def predict_customer(customer_data: dict):

    model, preprocessor = load_model()

    df = pd.DataFrame([customer_data])

    X = preprocessor.transform(df)

    prediction = model.predict(X)[0]

    probability = model.predict_proba(X)[0][1]

    confidence = probability if prediction == 1 else (1 - probability)

    return prediction, probability, confidence