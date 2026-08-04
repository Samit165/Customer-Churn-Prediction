@echo off
if exist "%~dp0churn_env\Scripts\python.exe" (
    "%~dp0churn_env\Scripts\python.exe" -m streamlit run app/app.py
) else (
    "C:\Users\samit\anaconda3\python.exe" -m streamlit run app/app.py
)
pause
