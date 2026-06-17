#!/usr/bin/env bash
set -euo pipefail
streamlit run app.py --server.address 0.0.0.0 --server.port "${PORT:-8888}"
