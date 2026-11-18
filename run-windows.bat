@echo off
rem Double-click to run the Baby Names app. The first run sets up its Python packages, which takes a few minutes.
cd /d "%~dp0"
if not exist .venv (
  py -3 -m venv .venv 2>nul || python -m venv .venv
)
if not exist .venv\Scripts\python.exe (
  echo Python 3 is needed. Install it from https://www.python.org/downloads/ and run this again.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m pip install --quiet --disable-pip-version-check -r requirements.txt
.venv\Scripts\python.exe -m streamlit run "drive-download-20240113T005539Z-001\main\app.py"
pause
