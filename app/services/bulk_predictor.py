import joblib
import pandas as pd

from core.config import MODEL_PATH, PREPROCESSOR_PATH


def load_model_artifacts():
    """Load model artifacts using the project-configured paths."""
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    return model, preprocessor


# Load once when the application starts
model, preprocessor = load_model_artifacts()


def predict_bulk(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform bulk churn prediction.

    Returns the original dataframe with prediction,
    probability, confidence, risk level, and recommendation.
    """

    input_df = df.copy()

    # Safely convert numeric columns
    numeric_cols = [
        "Tenure Months",
        "Monthly Charges",
        "Total Charges",
    ]

    for col in numeric_cols:
        if col in input_df.columns:
            input_df[col] = (
                pd.to_numeric(
                    input_df[col],
                    errors="coerce"
                )
                .fillna(0)
            )

    # Preprocess
    processed_data = preprocessor.transform(input_df)

    # Model predictions
    predictions = model.predict(processed_data)

    probabilities = model.predict_proba(
        processed_data
    )[:, 1]

    result_df = df.copy()

    # -----------------------------
    # Prediction
    # -----------------------------
    result_df["Prediction"] = [
        "Churn" if prediction == 1 else "No Churn"
        for prediction in predictions
    ]

    # -----------------------------
    # Probability
    # -----------------------------
    result_df["Probability"] = (
        probabilities * 100
    ).round(2)

    # -----------------------------
    # Confidence
    # Same logic as predict.py
    # -----------------------------
    confidences = [
        probability if prediction == 1
        else (1 - probability)
        for prediction, probability
        in zip(predictions, probabilities)
    ]

    result_df["Confidence"] = [
        round(c * 100, 2) for c in confidences
    ]

    # -----------------------------
    # Risk Level
    # -----------------------------
    result_df["Risk Level"] = [
        "HIGH" if prediction == 1 else "LOW"
        for prediction in predictions
    ]

    # -----------------------------
    # Recommendation
    # -----------------------------
    result_df["Recommendation"] = [
        (
            "Contact the customer immediately and "
            "offer a retention incentive."
        )
        if prediction == 1
        else (
            "Customer is likely to remain. "
            "Continue normal engagement."
        )
        for prediction in predictions
    ]

    return result_df