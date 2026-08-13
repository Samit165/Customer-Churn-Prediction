import pandas as pd


# Required columns for the trained model
REQUIRED_COLUMNS = [
    "City",
    "Gender",
    "Senior Citizen",
    "Partner",
    "Dependents",
    "Tenure Months",
    "Phone Service",
    "Multiple Lines",
    "Internet Service",
    "Online Security",
    "Online Backup",
    "Device Protection",
    "Tech Support",
    "Streaming TV",
    "Streaming Movies",
    "Contract",
    "Paperless Billing",
    "Payment Method",
    "Monthly Charges",
    "Total Charges",
]


def validate_csv(df: pd.DataFrame):
    """
    Validate uploaded customer dataset.

    Returns:
        (bool, message)
    """

    if df.empty:
        return False, "The uploaded CSV is empty."

    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:
        return (
            False,
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    return True, "Validation successful."