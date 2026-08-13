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

    Returns the original dataframe with prediction columns added.
    """
    input_df = df.copy()

    # Safely convert numeric columns, replacing missing/blank values with 0
    numeric_cols = ["Tenure Months", "Monthly Charges", "Total Charges"]
    for col in numeric_cols:
        if col in input_df.columns:
            input_df[col] = pd.to_numeric(input_df[col], errors="coerce").fillna(0)

    # Preprocess
    processed_data = preprocessor.transform(input_df)

    # Predictions
    predictions = model.predict(processed_data)
    probabilities = model.predict_proba(processed_data)[:, 1]

    result_df = df.copy()

    result_df["Prediction"] = [
        "Churn" if p == 1 else "No Churn"
        for p in predictions
    ]

    result_df["Probability"] = (
        probabilities * 100
    ).round(2)

    return result_df