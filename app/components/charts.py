import plotly.express as px
import pandas as pd


def churn_pie():
    df = pd.DataFrame({
        "Status": ["Stayed", "Churned"],
        "Customers": [735, 265]
    })

    fig = px.pie(
        df,
        values="Customers",
        names="Status",
        hole=0.55
    )

    fig.update_layout(
        height=350,
        margin=dict(l=10, r=10, t=40, b=10)
    )

    return fig


def prediction_trend():

    df = pd.DataFrame({
        "Day": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        "Predictions":[25,31,29,42,38,46,51]
    })

    fig = px.line(
        df,
        x="Day",
        y="Predictions",
        markers=True
    )

    fig.update_layout(height=350)

    return fig


def model_performance():

    df = pd.DataFrame({
        "Model":["Logistic","Random Forest","XGBoost"],
        "Accuracy":[81.2,84.3,85.7]
    })

    fig = px.bar(
        df,
        x="Model",
        y="Accuracy"
    )

    fig.update_layout(height=350)

    return fig