#!/usr/bin/env bash
set -euo pipefail

# Renku sessions/jobs clone repositories below /home/renku/work/<repo-name>.
# Depending on how the image command is started, the current working directory may
# be /home/renku/work rather than the repository root. Make the script robust.
if [[ ! -d "src/mnist_jobs" && -d "/home/renku/work/pi-gpt-ml-demo-jobs/src/mnist_jobs" ]]; then
  cd /home/renku/work/pi-gpt-ml-demo-jobs
fi

export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

# Renku serves interactive sessions below /sessions/<session-name>/ and the
# current auth proxy setup does not rewrite paths before forwarding to Streamlit.
# Configure Streamlit with the same base path so its HTML, static assets, and
# websocket endpoints resolve correctly.
BASE_URL_PATH="${STREAMLIT_BASE_URL_PATH:-}"
if [[ -z "${BASE_URL_PATH}" && -n "${JUPYTERHUB_SERVICE_PREFIX:-}" ]]; then
  BASE_URL_PATH="${JUPYTERHUB_SERVICE_PREFIX#/}"
  BASE_URL_PATH="${BASE_URL_PATH%/}"
fi
if [[ -z "${BASE_URL_PATH}" && -n "${RENKU_SESSION_URL:-}" ]]; then
  BASE_URL_PATH="${RENKU_SESSION_URL#*://*/}"
  BASE_URL_PATH="${BASE_URL_PATH%/}"
fi
if [[ -z "${BASE_URL_PATH}" && -n "${HOSTNAME:-}" ]]; then
  BASE_URL_PATH="sessions/${HOSTNAME}"
fi

printf 'Dashboard cwd: %s\n' "${PWD}"
printf 'Dashboard baseUrlPath: %s\n' "${BASE_URL_PATH}"
printf 'Relevant environment variables:\n'
env | sort | grep -E '^(RENKU|JUPYTER|SESSION|HOSTNAME|AMALTHEA|STREAMLIT)=' || true

args=(
  run app.py
  --server.address 0.0.0.0
  --server.port "${PORT:-8888}"
  --server.headless true
  --server.enableCORS false
  --server.enableXsrfProtection false
  --browser.gatherUsageStats false
)

if [[ -n "${BASE_URL_PATH}" ]]; then
  args+=(--server.baseUrlPath "${BASE_URL_PATH}")
fi

streamlit "${args[@]}"
