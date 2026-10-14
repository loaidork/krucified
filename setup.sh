#!/usr/bin/env bash
# krucified — setup (Linux)
set -e
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
echo "[*] creating virtualenv (.venv)..."
"$PY" -m venv .venv
echo "[*] installing dependencies..."
./.venv/bin/pip install --upgrade pip >/dev/null
./.venv/bin/pip install -r requirements.txt
echo "[+] done. run ./start.sh"
