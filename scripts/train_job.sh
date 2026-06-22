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

# Give the cloud-storage mount time to flush model artifacts before the job pod
# terminates. This is especially important for Polybox/SWITCHdrive-backed
# connectors: the training process can finish before the sidecar/backend has
# made the new checkpoint visible to other sessions, such as the dashboard.
SYNC_DELAY_SECONDS="${MODEL_SYNC_DELAY_SECONDS:-60}"
echo "Training finished; flushing filesystem and waiting ${SYNC_DELAY_SECONDS}s for model storage sync..."
sync || true
sleep "${SYNC_DELAY_SECONDS}"
echo "Model storage sync grace period complete."
