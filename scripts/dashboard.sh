#!/usr/bin/env bash
set -euo pipefail

# Renku sessions/jobs clone repositories below /home/renku/work/<repo-name>.
# Depending on how the image command is started, the current working directory may
# be /home/renku/work rather than the repository root. Make the script robust.
if [[ ! -d "src/mnist_jobs" && -d "/home/renku/work/pi-gpt-ml-demo-jobs/src/mnist_jobs" ]]; then
  cd /home/renku/work/pi-gpt-ml-demo-jobs
fi

export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

streamlit run app.py --server.address 0.0.0.0 --server.port "${PORT:-8888}"
