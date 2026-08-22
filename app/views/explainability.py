import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt  # pyright: ignore[reportMissingModuleSource]


MODEL_PATH = "models/churn_model.pkl"
PREPROCESSOR_PATH = "models/preprocessor.pkl"
X_TEST_PATH = "data/processed/X_test_processed.pkl"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_resource
def load_preprocessor():
    return joblib.load(PREPROCESSOR_PATH)


@st.cache_data
def load_test_data():
    return joblib.load(X_TEST_PATH)


@st.cache_resource
def create_explainer():
    model = load_model()
    return shap.TreeExplainer(model)


def prepare_test_data():
    preprocessor = load_preprocessor()
    X_test_processed = load_test_data()

    feature_names = [
        name.replace("cat__", "").replace("num__", "")
        for name in preprocessor.get_feature_names_out()
    ]

    if hasattr(X_test_processed, "toarray"):
        X_test_processed = X_test_processed.toarray()

    X_test_processed = pd.DataFrame(
        X_test_processed,
        columns=feature_names
    )

    return X_test_processed, feature_names


def render():

    st.title("🧩 Model Explainability")

    st.caption(
        "Understand why ChurnGuard makes its customer churn predictions "
        "using SHAP."
    )

    try:

        model = load_model()
        X_test_processed, feature_names = prepare_test_data()
        explainer = create_explainer()

        st.success("SHAP explainability engine loaded successfully.")

        st.markdown("---")

        st.subheader("🔍 Customer Explanation")

        customer_index = st.number_input(
            "Select Customer Index",
            min_value=0,
            max_value=len(X_test_processed) - 1,
            value=0,
            step=1
        )

        customer = X_test_processed.iloc[[customer_index]]

        prediction = model.predict(customer)[0]

        probability = model.predict_proba(customer)[0, 1]

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

        st.markdown("---")

        st.subheader("📊 Why did the model make this prediction?")

        shap_values = explainer(customer)

        fig, ax = plt.subplots(figsize=(10, 6))

        shap.plots.waterfall(
            shap_values[0],
            max_display=15,
            show=False
        )

        st.pyplot(fig, clear_figure=True)

        plt.close(fig)

    except Exception as e:

        st.error(
            "Unable to load the SHAP explainability module."
        )

        st.exception(e)