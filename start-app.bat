@echo off

REM Change to the directory where the script is located
cd /d %~dp0

IF NOT EXIST .env (
    python -m venv .env
    cd .env\Scripts
    call activate.bat
    cd ../..
    pip install -r requirements.txt
) ELSE (
    cd .env\Scripts
    call activate.bat
    cd ../..
)

streamlit run menu.py
