if (Test-Path "$PSScriptRoot\churn_env\Scripts\python.exe") {
    & "$PSScriptRoot\churn_env\Scripts\python.exe" -m streamlit run app/app.py
} else {
    & "C:\Users\samit\anaconda3\python.exe" -m streamlit run app/app.py
}
