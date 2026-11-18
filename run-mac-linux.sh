#!/bin/sh
# Run the Baby Names app: sh run-mac-linux.sh. The first run sets up its Python packages, which takes a few minutes.
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt
exec .venv/bin/python -m streamlit run "drive-download-20240113T005539Z-001/main/app.py"
