start cmd /k "cd /d %~dp0api && uvicorn app:app --reload"
start cmd /k "cd /d %~dp0interface && streamlit run app.py"
