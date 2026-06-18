#!/usr/bin/env bash
set -euo pipefail

# Renku sessions clone repositories below /home/renku/work/<repo-name>.
# Prefer the runtime clone so dashboard-only code changes do not require an image rebuild.
if [[ -d "/home/renku/work/pi-gpt-ml-demo-jobs/src/mnist_jobs" ]]; then
  cd /home/renku/work/pi-gpt-ml-demo-jobs
fi

export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

HOST="${RENKU_SESSION_IP:-0.0.0.0}"
PORT="${RENKU_SESSION_PORT:-${PORT:-8888}}"
BASE_URL_PATH="${RENKU_BASE_URL_PATH:-}"
# Streamlit expects server.baseUrlPath without a leading slash.
BASE_URL_PATH="${BASE_URL_PATH#/}"
BASE_URL_PATH="${BASE_URL_PATH%/}"

printf 'Dashboard cwd: %s\n' "${PWD}"
printf 'Dashboard host: %s\n' "${HOST}"
printf 'Dashboard port: %s\n' "${PORT}"
printf 'Dashboard baseUrlPath: %s\n' "${BASE_URL_PATH}"
printf 'Relevant environment variables:\n'
env | sort | grep -E '^(RENKU|JUPYTER|SESSION|HOSTNAME|AMALTHEA|STREAMLIT)=' || true

args=(
  run app.py
  --server.address "${HOST}"
  --server.port "${PORT}"
  --server.headless true
  --server.enableCORS false
  --server.enableXsrfProtection false
  --browser.gatherUsageStats false
)

if [[ -n "${BASE_URL_PATH}" ]]; then
  args+=(--server.baseUrlPath "${BASE_URL_PATH}")
fi

streamlit "${args[@]}"
