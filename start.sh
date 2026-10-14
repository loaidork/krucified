#!/usr/bin/env bash
# krucified — launcher (Linux)
cd "$(dirname "$0")"
if [ -x "./.venv/bin/python" ]; then
    exec ./.venv/bin/python krucified.py
else
    exec "${PYTHON:-python3}" krucified.py
fi
