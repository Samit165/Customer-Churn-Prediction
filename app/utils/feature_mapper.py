import re


RAW_FEATURES = [
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


def map_shap_feature(feature_name: str, customer_data: dict):
    """
    Convert a transformed SHAP feature name into a
    human-readable feature name and original customer value.
    """

    # Remove preprocessing prefixes if present
    clean_name = re.sub(r"^(cat|num)__", "", feature_name)

    # ---------------------------------------------------------
    # Numerical features
    # ---------------------------------------------------------

    if clean_name in customer_data:

        value = customer_data[clean_name]

        return clean_name, value

    # ---------------------------------------------------------
    # One-hot encoded categorical features
    # ---------------------------------------------------------

    for raw_feature in RAW_FEATURES:

        prefix = f"{raw_feature}_"

        if clean_name.startswith(prefix):

            category = clean_name[len(prefix):]

            return raw_feature, category

    # ---------------------------------------------------------
    # Fallback
    # ---------------------------------------------------------

    return clean_name, None


def format_customer_value(feature_name: str, value):

    if value is None:
        return ""

    if feature_name == "Monthly Charges":
        return f"${float(value):,.2f}"

    if feature_name == "Total Charges":
        return f"${float(value):,.2f}"

    if feature_name == "Tenure Months":
        return f"{value} months"

    return str(value)


def get_display_name(feature_name: str, customer_data: dict):

    base_name, value = map_shap_feature(
        feature_name,
        customer_data
    )

    formatted_value = format_customer_value(
        base_name,
        value
    )

    if formatted_value:
        return f"{base_name}: {formatted_value}"

    return base_name