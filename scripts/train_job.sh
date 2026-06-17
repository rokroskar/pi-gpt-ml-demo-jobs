#!/usr/bin/env bash
set -euo pipefail

# Renku sessions/jobs clone repositories below /home/renku/work/<repo-name>.
# Depending on how the image command is started, the current working directory may
# be /home/renku/work rather than the repository root. Make the script robust.
if [[ ! -d "src/mnist_jobs" && -d "/home/renku/work/pi-gpt-ml-demo-jobs/src/mnist_jobs" ]]; then
  cd /home/renku/work/pi-gpt-ml-demo-jobs
fi

export PYTHONPATH="${PWD}/src:${PYTHONPATH:-}"

python -m mnist_jobs.train \
  --data-dir "${MNIST_DATA_DIR:-/home/renku/work/mnist-dataset-doi-10.5281-zenodo.10058130}" \
  --model-dir "${MODEL_DIR:-/home/renku/work/models}" \
  --target-accuracy "${TARGET_ACCURACY:-0.99}"
